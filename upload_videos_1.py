#!/usr/bin/python

# Usage example:
# python playlist_localizations.py --action='<action>' --playlist_id='<playlist_id>' --default_language='<default_language>' --language='<language>' --title='<title>' --description='<description>'
from datetime import datetime
import os
from re import S
from unicodedata import category
import httplib2
import google.oauth2.credentials
import google_auth_oauthlib.flow
import random
import sys
import time
import subprocess
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

httplib2.RETRIES = 1

# Maximum number of times to retry before giving up.
MAX_RETRIES = 10

# Always retry when these exceptions are raised.
RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError)
VALID_PRIVACY_STATUSES = ("public", "private", "unlisted")

# Always retry when an apiclient.errors.HttpError with one of these status
# codes is raised.
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]
# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains

# the OAuth 2.0 information for this application, including its client_id and
# client_secret. You can acquire an OAuth 2.0 client ID and client secret from
# the {{ Google Cloud Console }} at
# {{ https://cloud.google.com/console }}.
# Please ensure that you have enabled the YouTube Data API for your project.
# For more information about using OAuth2 to access the YouTube Data API, see:
#   https://developers.google.com/youtube/v3/guides/authentication
# For more information about the client_secrets.json file format, see:
#   https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
f = open("count_api.txt", "w")
f.write(str((int(sys.argv[8]))))
f.close()
CLIENT_SECRETS_FILE = 'client_secrets'+sys.argv[8]+'.json'
print(CLIENT_SECRETS_FILE)

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account.
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
SCOPES1 = ["https://www.googleapis.com/auth/youtube.upload"]
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

ACTIONS = ('get', 'list', 'set')
MISSING_CLIENT_SECRETS_MESSAGE ="""
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:

   %s

with information from the API Console
https://console.developers.google.com/

For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   CLIENT_SECRETS_FILE))
# Authorize the request and store authorization credentials.
def get_authenticated_service(args):
  flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
    scope=SCOPES,
    message=MISSING_CLIENT_SECRETS_MESSAGE)
  args.noauth_local_webserver = False
  storage = Storage("%s-oauth2.json" % (sys.argv[0]+sys.argv[8]))
  credentials = storage.get()

  if credentials is None or credentials.invalid:
    credentials = run_flow(flow, storage, args)

  return build(API_SERVICE_NAME,API_VERSION,
    http=credentials.authorize(httplib2.Http()))

# Call the API's playlists.update method to update an existing playlist's default language,
# localized title and description in a specific language.
def initialize_upload(youtube, options):
  tags = None
  if options.keywords:
    tags = options.keywords.split(",")

  body=dict(
    snippet=dict(
      title=options.title,
      description=options.description,
      tags=tags,
      categoryId=options.category,
      datetime=options.publishedAt
    ),
    status=dict(
      privacyStatus=options.privacyStatus,
      publishAt=options.publishAt
    )
  )

  # Call the API's videos.insert method to create and upload the video.
  insert_request = youtube.videos().insert(
    part=",".join(body.keys()),
    body=body,
    # The chunksize parameter specifies the size of each chunk of data, in
    # bytes, that will be uploaded at a time. Set a higher value for
    # reliable connections as fewer chunks lead to faster uploads. Set a lower
    # value for better recovery on less reliable connections.
    #
    # Setting "chunksize" equal to -1 in the code below means that the entire
    # file will be uploaded in a single HTTP request. (If the upload fails,
    # it will still be retried where it left off.) This is usually a best
    # practice, but if you're using Python older than 2.6 or if you're
    # running on App Engine, you should set the chunksize to something like
    # 1024 * 1024 (1 megabyte).
    media_body=MediaFileUpload(args.file, chunksize=-1, resumable=True)
  )

  resumable_upload(youtube,insert_request)
def resumable_upload(youtube,insert_request):
  response = None
  error = None
  retry = 0
  while response is None:
    try:
      print ("Uploading file...")
      status, response = insert_request.next_chunk()
      if response is not None:
        if 'id' in response:
          print ("Video id '%s' was successfully uploaded." % response['id'])
          youtube.thumbnails().set(
          videoId=response['id'],
          media_body="D:/Python/youtube_client/"+sys.argv[20]+'_1.jpg'
          ).execute()
          
          
          
          
        else:
          exit("The upload failed with an unexpected response: %s" % response)
    except HttpError as e:
      if e.resp.status in RETRIABLE_STATUS_CODES:
        error = "A retriable HTTP error %d occurred:\n%s" % (e.resp.status,
                                                             e.content)
      else:
        raise
    except RETRIABLE_EXCEPTIONS as e:
      error = "A retriable error occurred: %s" % e

    if error is not None:
      print (error)
      retry += 1
      if retry > MAX_RETRIES:
        exit("No longer attempting to retry.")

      max_sleep = 2 ** retry
      sleep_seconds = random.random() * max_sleep
      print ("Sleeping %f seconds and then retrying..." % sleep_seconds)
      time.sleep(sleep_seconds)
if __name__ == '__main__':
 
  # The action to be processed: 'get', 'list', and 'set' are supported.
  argparser.add_argument("--file", required=True, help="Video file to upload")
  argparser.add_argument('--action', required=True, help='Action', choices=ACTIONS)
  # The ID of the selected YouTube olaylist.
  argparser.add_argument('--playlist_id',
    help='The playlist ID for which localizations are being set or retrieved.',
    required=True)
  # The langauge of the playlist's default metadata.
  argparser.add_argument('--default_language',
    help='Default language to set for the playlist.')
  # The language of the localization that is being set or retrieved.
  argparser.add_argument('--language', help='Language of the localization.')
  # The localized title to set in the specified language.
  argparser.add_argument('--title',
    help='Localized title to be set for the playlist.',
    default='Localized Title')
  # The localized description to set in the specified language.
  argparser.add_argument('--description',
    help='Localized description to be set for the playlist.',
    default='Localized Description')
  argparser.add_argument('--c',
    help='Localized description to be set for the playlist.')
  argparser.add_argument('--n_v',
    help='Localized description to be set for the playlist.')
  argparser.add_argument('--publishedAt',
    help='Localized description to be set for the playlist.',default=sys.argv[14])
  argparser.add_argument("--privacyStatus", choices=VALID_PRIVACY_STATUSES,
    default=VALID_PRIVACY_STATUSES[1], help="Video privacy status.")
  argparser.add_argument("--publishAt",default=sys.argv[16])
  argparser.add_argument("--keywords", help="Video keywords, comma separated",
    default=sys.argv[18])
  argparser.add_argument("--category", default=sys.argv[22],
  help="Numeric video category. " +
  "See https://developers.google.com/youtube/v3/docs/videoCategories/list")

  args = argparser.parse_args()

  youtube = get_authenticated_service(args)

  try:
    if args.action == 'set':
      initialize_upload(youtube, args)
  except HttpError as e:
    print ('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))
    action1="set"
    play_list="PLQ_BzM_Cvnku-SA2R31DT09fSYvoRAp07"
    print(str(int(sys.argv[8])+1))
    subprocess.Popen(['python', 'upload_videos_1.py', '--file',
    sys.argv[2], '--action',action1,'--playlist_id',play_list,'--c', str(int(sys.argv[8])+1),
    '--title',sys.argv[10],'--description',sys.argv[12],'--publishedAt',sys.argv[14],'--publishAt',sys.argv[16],
    '--keywords',sys.argv[18],'--n_v',sys.argv[20],'--category',sys.argv[22]])
    