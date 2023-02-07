// Copyright (C) 2023 Assistance.Chat contributors

// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at

//     http://www.apache.org/licenses/LICENSE-2.0

// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

import { contactUs, ContactUsData } from "assistance";

import { ChatContextData } from "@/providers/chat";

export async function callContactUsApi(chatData: ChatContextData) {
  const clientData = chatData.originatorDetails.client;

  if (
    !clientData.agreeToTerms ||
    !clientData.email ||
    !clientData.phoneNumber ||
    !clientData.firstName ||
    !clientData.lastName ||
    !clientData.enquiryMessage
  ) {
    return;
  }

  const contactUsData: ContactUsData = {
    first_name: clientData.firstName,
    last_name: clientData.lastName,
    email: clientData.email,
    phone_number: clientData.phoneNumber,
    message: clientData.enquiryMessage,
    agree_to_terms: clientData.agreeToTerms,
  };

  if (clientData.referrerTag) {
    contactUsData.referrer_tag = clientData.referrerTag;
  }

  const response = await contactUs(contactUsData);
  console.log(response);
}
