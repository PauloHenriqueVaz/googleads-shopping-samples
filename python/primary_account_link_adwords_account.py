#!/usr/bin/python
#
# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Links the specified AdWords account to the specified merchant center account.
"""

import sys

from oauth2client import client
import shopping_common


def main(argv):
  # Authenticate and construct service.
  service, config, _ = shopping_common.init(argv, __doc__)
  merchant_id = config['merchantId']
  adwords_id = None
  if shopping_common.json_absent_or_false(config, 'accountSampleAdWordsCID'):
    print 'Must specify the AdWords CID to link in the samples configuration.'
    sys.exit(1)
  adwords_id = config['accountSampleAdWordsCID']

  try:
    # First we need to retrieve the existing set of users.
    response = service.accounts().get(merchantId=merchant_id,
                                      accountId=merchant_id,
                                      fields='adwordsLinks').execute()

    account = response

    # Add new user to existing user list.
    adwords_link = {'adwordsId': adwords_id, 'status': 'active'}
    account.setdefault('adwordsLinks', []).append(adwords_link)

    # Patch account with new user list.
    response = service.accounts().patch(merchantId=merchant_id,
                                        accountId=merchant_id,
                                        body=account).execute()

    print 'AdWords ID %s was added to merchant ID %s' % (adwords_id,
                                                         merchant_id)

  except client.AccessTokenRefreshError:
    print ('The credentials have been revoked or expired, please re-run the '
           'application to re-authorize')

if __name__ == '__main__':
  main(sys.argv)
