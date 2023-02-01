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

import { ChatContextData } from "@/providers/chat";

export async function callChatApi(chatContext: ChatContextData) {
  const agentName = chatContext.originatorNames.agent || "{agent_name}";
  const taskPrompt = chatContext.taskPrompt;

  let transcript = "";
  for (let item of chatContext.messageHistory) {
    const name = chatContext.originatorNames[item.originator];
    const message = item.message;

    transcript += `${name}: ${message}\n\n`;
  }

  let data: ApiChatData = {
    agent_name: agentName,
    task_prompt: chatContext.taskPrompt,
    transcript: transcript,
  };

  if (chatContext.googleIdToken) {
    data.google_id_token = chatContext.googleIdToken;
  }

  if (chatContext.assistanceToken) {
    data.assistance_token = chatContext.assistanceToken;
  }

  return await chat(data);
}
