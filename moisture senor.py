#
# Copyright 2010-2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# This file is licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License. A copy of
# the License is located at
#
# http://aws.amazon.com/apache2.0/
#
# This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
#


from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import RPi.GPIO as GPIO
import time
import random, time

# A random programmatic shadow client ID.
SHADOW_CLIENT = "TestSensor"

# The unique hostname that AWS IoT generated for 
# this device.
HOST_NAME = "a3ritzv6ok1syh-ats.iot.us-east-1.amazonaws.com"

# The relative path to the correct root CA file for AWS IoT, 
# that you have already saved onto this device.
ROOT_CA = "amazon-roor-ca.pem"

# The relative path to your private key file that 
# AWS IoT generated for this device, that you 
# have already saved onto this device.
PRIVATE_KEY = "2dff22ebcc-private.pem.key"

# The relative path to your certificate file that 
# AWS IoT generated for this device, that you 
# have already saved onto this device.
CERT_FILE = "2dff22ebcc-certificate.pem.crt"

# A programmatic shadow handler name prefix.
SHADOW_HANDLER = "TestSensor"

# Automatically called whenever the shadow is updated.
def myShadowUpdateCallback(payload, responseStatus, token):
  print()
  print('UPDATE: $aws/things/' + SHADOW_HANDLER + 
    '/shadow/update/#')
  print("payload = " + payload)
  print("responseStatus = " + responseStatus)
  print("token = " + token)

# Create, configure, and connect a shadow client.
myShadowClient = AWSIoTMQTTShadowClient(SHADOW_CLIENT)
myShadowClient.configureEndpoint(HOST_NAME, 8883)
myShadowClient.configureCredentials(ROOT_CA, PRIVATE_KEY,
  CERT_FILE)
myShadowClient.configureConnectDisconnectTimeout(10)
myShadowClient.configureMQTTOperationTimeout(5)
myShadowClient.connect()

# Create a programmatic representation of the shadow.
myDeviceShadow = myShadowClient.createShadowHandlerWithName(
  SHADOW_HANDLER, True)

# Keep generating random test data until this script 
# stops running.
# To stop running this script, press Ctrl+C.
while True:
  # Generate random True or False test data to represent
  # okay or low moisture levels, respectively.
  moisture = random.choice([True, False])

  if moisture:
    myDeviceShadow.shadowUpdate(
      '{"state":{"reported":{"moisture":"okay"}}}',
      myShadowUpdateCallback, 5)
  else:
    myDeviceShadow.shadowUpdate(
      '{"state":{"reported":{"moisture":"low"}}}',
      myShadowUpdateCallback, 5)

  # Wait for this test value to be added.
  time.sleep(60)



