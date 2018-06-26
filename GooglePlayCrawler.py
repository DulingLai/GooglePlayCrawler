
import os
import csv
import time
import json
import psutil
import requests
import argparse
import subprocess
import gpcconstants

def download_single_apk(apk_id, apk_folder, index, total, force_overwrite, device_codename = 'hammerhead'):
    # remove existing APK
    if force_overwrite:
        if os.path.exists(apk_folder + '/' + apk_id + '.apk'): os.remove(apk_folder + '/' + apk_id + '.apk')
    else:
        if os.path.exists(apk_folder + '/' + apk_id + '.apk'):
            print('* ' + apk_folder + '/' + apk_id + '.apk' + ' exists! Not overwriting!')
            return True

    # download APK
    print("(" + str(index) + "/" + str(total) + ")" + " Downloading: " + apk_id)
    try:
        subprocess.check_output(['gplaycli','-d',apk_id,'-f',apk_folder, '-dc', device_codename])
    except subprocess.CalledProcessError as e:
        print("**** Failed to download due to error: ", e)
        return False
    
    if not os.path.exists(apk_folder + '/' + apk_id + ".apk"):
        print("**** Error occurred while downloading...")
        return False
    else: return True

def start_api_server(gscraper_dir):
    try:
        p = subprocess.Popen('npm start', cwd=gscraper_dir,shell=True,preexec_fn=os.setsid)
    except subprocess.CalledProcessError as e:
        print("Failed to download due to error: ", e)

def stop_api_server():
    for proc in psutil.process_iter():
        # check whether the process name matches
        if proc.name() == 'node':
            proc.kill()

def get_app_by_collection_category(collection, category, num, start):
    # get the list of top apps
    if category=='NONE':
        request_params = {'collection':collection, 'num':num, 'start':start, 'country':'ca'}
    else:
        request_params = {'collection':collection, 'category':category, 'num':num, 'start':start, 'country':'ca'}    
    r = requests.get('http://localhost:3000/api/apps/', params=request_params)
    
    # if we successfully get the response
    if(r.ok):
        app_list = r.json().get('results')
        app_id_list = [app.get('appId') for app in app_list]
        return app_id_list
    else:
        # If response code is not ok (200), print the resulting http error code with description
        r.raise_for_status()

def download_batch_app(apk_folder, collection, category, num, start, device_code, force_overwrite):
    # start the server as we need to query information of each app
    start_api_server(gpcconstants.GSCRAPPER_DIR)
    time.sleep(1)

    # get the lost of apps
    app_list = get_app_by_collection_category(collection, category, num, start)
    
    # variables to store app information which will be written to a csv file after we are done with one category
    app_info = {}
    
    # loop variables
    num_apps = len(app_list)
    index = 1
    
    # for each app in the app list: download the app and store the app information
    for app in app_list:
        if not download_single_apk(app, apk_folder, index, num_apps, force_overwrite, device_code):
            app_info[app]=["Download Error"]
        else:
            complete_app_info=requests.get('http://localhost:3000/api/apps/'+app).json()
            app_info[app] = [complete_app_info.get('title'),complete_app_info.get('genreId'),complete_app_info.get('size'),complete_app_info.get('version'),complete_app_info.get('installs'),complete_app_info.get('scoreText'),complete_app_info.get('ratings'),complete_app_info.get('androidVersionText')]
        index = index + 1
    
    # stop the server
    stop_api_server()

    # write the collected app information to a csv file
    with open(apk_folder+'/app_info.csv','w+') as reportFile:
        wr = csv.writer(reportFile, dialect='excel')
        for app in app_info.keys():
            wr.writerow([app] + app_info.get(app))

if __name__ == '__main__':
    # construct the argument parser
    ap = argparse.ArgumentParser(description='Download batch apks from Google Play Store.')
    ap.add_argument('-d','--dir', required=True, help='The folder to store the downloaded APKs (required)')
    ap.add_argument('-f','--force_overwrite', nargs='?', const=True, default=False, type=bool, help='Option to overwrite the existing APKs in the directiory (default: diabled)')
    ap.add_argument('-a','--all', nargs='?', const=True, default=False,type=bool, help='Set this option to True will download all categories (default: False)')
    ap.add_argument('-c','--collection', nargs='?', default='TOP_FREE', help='The collection to download from {TOP_FREE,NEW_FREE,GROSSING,TRENDING} (default: TOP_FREE)')
    ap.add_argument('-g','--category', nargs='?', default='NONE', help='The category to download (default: NONE; Available options can be found in documentation).')
    ap.add_argument('-n','--number', nargs='?', default='120', help='The number of apps to download (default: 120; Max: 120).')
    ap.add_argument('-s','--start', nargs='?', default='0', help='The starting index of the retrieved list (default: 0; Max: 500)')
    ap.add_argument('-dc','--device_code', nargs='?',const='hammerhead', default='hammerhead', help='The target device of the download apps (default: hammerhead)')
    
    # parse the arguments
    args = vars(ap.parse_args())
    apk_folder = args['dir']
    force_overwrite = args['force_overwrite']
    download_all = args['all']
    collection = gpcconstants.COLLECTION.get(args['collection'])
    category = gpcconstants.CATEGORY.get(args['category'])
    number = args['number']
    start = args['start']
    device_code = args['device_code']
    
    # get the app list
    if download_all:
        print("Downloading all possible categories")
        for category in gpcconstants.CATEGORY:
            apk_folder_new = os.path.join(apk_folder, category)
            if not os.path.exists(apk_folder_new):
                os.makedirs(apk_folder_new)
            download_batch_app(apk_folder_new, collection, category, number, start, device_code, force_overwrite)
    else:
        download_batch_app(apk_folder, collection, category, number, start, device_code, force_overwrite)