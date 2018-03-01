import requests
import json
import configparser
import shutil
import datetime
import os
import argparse
import polling


def parse_config(configfile="settings.cfg"):
    '''
    Function to read all the config settings from the configuration file.
    :param str configfile: path to the configuration file
    :returns dictionary with all configuration data
    '''
    config = configparser.ConfigParser()
    config.read('settings.cfg')
    token = config.get('authentication','token')
    round_id = config.get('authentication','round_id')

    source_dir = config.get('project','source_dir')

    dataset_ids = [config.get('datasets','dataset'+str(i)) for i in range(4)]
    solutions = [config.get('project','solutions'+str(i)) for i in range(4)]

    topscore_dir = "topscores"

    return {"token":token,
            "round_id":round_id,
            "source_dir":source_dir,
            "dataset_ids":dataset_ids,
            "solutions":solutions,
            "topscore_dir":topscore_dir}

class APICommunicator:
    '''
    Class that handles all communication with the hashcodejudge API
    '''

    def __init__(self,token, round_id):
        self.token = token
        self.round_id = round_id
        self.base_url = "https://hashcode-judge.appspot.com/api/judge/v1/"

    def check_submission(self, submitted):
        '''
        Checks the result of the submitted solution
        :param str token: authentication token
        :param str round_id: the current round_id
        :param str submitted:
        :returns dictionary with all configuration data
        '''
        print('.', sep=' ', end='', flush=True)
        url = self.base_url + "submissions/"+self.round_id
        headers = {
            'authorization': "Bearer " + self.token,
            'content-type': "application/json;charset=utf-8",
        }
        try:
            init_res = requests.get(url, headers=headers, allow_redirects=False)
            if init_res.status_code == 200:
                items = init_res.json()['items']
                current = [t for t in items if t["id"] == submitted]
                if len(current) != 0:
                    return {'scored':current[0]["scored"],'valid':current[0]["valid"],'best':current[0]["best"],'score':current[0]["score"]}
                print("Could not retrieve result")
                return None

            else:
                print("URL has not been created, your token might be expired.")
                return None
        except Exception as ce:
            print("ERROR: " + str(ce))

    def createUrl(self):
        '''
        Helper function for uploading a file. Retrieve URL to upload file
        :returns str
        :returns None if something went wrong
        '''
        url = self.base_url + "upload/createUrl"
        headers = {
            'authorization': "Bearer " + self.token,
            'content-type': "application/json;charset=utf-8",
        }

        try:
            init_res = requests.get(url, headers=headers, allow_redirects=False)
            if init_res.status_code == 200:
                return init_res.json()['value']
            else:
                print("URL has not been created, your token might be expired.")
                return None
        except Exception as ce:
            print("ERROR: " + str(ce))
            return None

    def upload(self,filename):
        '''
        Upload a file to the hashcodejudge API
        :param str filename: the path to the file to be uploaded
        :returns str: blob value
        :returns None if upload failed
        '''
        try:
            url = self.createUrl()
            if url is None:
                print("The file has not been succesfully uploaded. No upload url could be created.")
                return None
            with open(filename, 'rb') as file:
                response = requests.post(url, files={filename:file})
                if response.status_code == 200:
                    return response.json()[filename]
                else:
                    print("Something went wrong while uploading a file")
        except Exception as ce:
            print(ce)
            return None

    def submit(self,sourcesBlobKey,submissionBlobKey ,dataSet):
        '''
        Post submission with sources and submission for a certain dataset.
        :param str sourcesBlobKey: blob value retrieved by calling upload for the sources zip
        :param str submissionBlobKey: blob value retrieved by calling upload for the solution
        :param str dataSet: the dataset ID
        :returns int ID: the ID of the submission in the judge system
        :returns None if something failed
        '''
        url = self.base_url + "submissions"
        data={"dataSet":dataSet,"submissionBlobKey":submissionBlobKey,"sourcesBlobKey":sourcesBlobKey}
        headers = {
            'authorization': "Bearer " + self.token,
            'content-type': "application/json;charset=utf-8",
        }
        try:
            print("Submitting the solution.")
            response = requests.post(url,headers=headers,params=data)
            if response.status_code == 200:
                return response.json()
            else:
                print("Something went wrong while submitting")
                print(response.json())
                return None
        except Exception as ce:
            print(ce)
            return None


    def poll_submission(self,submission_id):
        '''
        Check for the submission until it is scored

        :param int submission_id: The submission ID
        :returns dict containing {score, scored, best, valid}
        '''
        print('Awaiting results', sep=' ', end='', flush=True)
        try:
            polling.poll(
                lambda: self.check_submission(submission_id).get("scored") == True,
                step=5,
                timeout=30
                )
            return self.check_submission(submission_id)
        except polling.TimeoutException as e:
            print("\nTimed out...")
            return None


def zipdir(path, outputfilename):
    try:
        shutil.make_archive(outputfilename, 'zip', path)
        return True
    except Exception as ce:
        return False

if __name__ == '__main__':
    config = parse_config()
    if not os.path.exists(config['topscore_dir']):
        os.mkdir(config['topscore_dir'])


    source_zipfile = 'source_'+str(datetime.datetime.now().isoformat())
    zipped = zipdir(config['source_dir'], source_zipfile )
    parser = argparse.ArgumentParser(description='Submit a solution')
    parser.add_argument('dataset_id', metavar='ID', type=int, nargs=1,
                   help='the ID of the dataset')
    parser.add_argument('--solution', dest='solution', nargs='?',
                    help='path to the solution file, overrides the config setting')
    args = parser.parse_args()

    solution_id = args.dataset_id[0]

    solutionfile = config['solutions'][solution_id]
    if args.solution is not None:
        solutionfile = args.solution

    API  = APICommunicator(config['token'], config['round_id'])

    if zipped and os.path.exists(solutionfile):
        sources=API.upload(source_zipfile+".zip")
        solution=API.upload(solutionfile)

        if sources is not None and solution is not None:
            submitted = API.submit(sources,solution,config['dataset_ids'][solution_id])['id']
            score = API.poll_submission(submitted)
            if score is not None:
                if score.get("best"):
                    print("You have increased your top score!!")
                    shutil.move(source_zipfile+".zip", config['topscore_dir'] + "/"+str(solution_id)+"-[" + score.get("score") + "].zip") # MOVE TO TOPSCORES
                if not score.get("valid"):
                    print("The submitted solution was declared invalid.")
                    os.remove(source_zipfile+".zip") # cleanup
                else:
                    print("Score: " +  score.get("score"))
            else:
                print("Received unexpected result.")
        else:
            print("Files have not been submitted.")
            os.remove(source_zipfile+".zip") # cleanup

    else:
        print("Something went wrong when retrieving the source and solution files, exiting now...")
