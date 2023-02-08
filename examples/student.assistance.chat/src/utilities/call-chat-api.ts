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

import { chat, ChatData as ApiChatData } from "assistance";

import { ChatContextData, MessageOriginator } from "@/providers/chat";

export async function callChatApi(
  chatData: ChatContextData,
  setChatData: (chatData: ChatContextData) => void
) {
  const agentName =
    chatData.originatorDetails.agent.firstName || "{agent_name}";

  let transcript = "";
  for (let item of chatData.messageHistory) {
    const name = chatData.originatorDetails[item.originator].firstName;
    const message = item.message;

    transcript += `${name}: ${message}\n\n`;
  }

  let apiData: ApiChatData = {
    agent_name: agentName,
    task_prompt: chatData.taskPrompt,
    transcript: transcript,
  };

  if (chatData.googleIdToken) {
    apiData.google_id_token = chatData.googleIdToken;
  }

  if (chatData.assistanceToken) {
    apiData.assistance_token = chatData.assistanceToken;
  }

  const chatResponse = await chat(apiData);

  const updatedMessageHistory = [
    ...chatData.messageHistory,
    {
      originator: "agent" as MessageOriginator,
      message: chatResponse.agent_message,
      timestamp: Date.now(),
    },
  ];

  const updatedChatData = {
    ...chatData,
    messageHistory: updatedMessageHistory,
    assistanceToken: chatResponse.assistance_token,
  };

  setChatData(updatedChatData);
}
