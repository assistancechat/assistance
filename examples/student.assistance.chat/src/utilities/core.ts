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

import { ChatContextData, Details } from "@/providers/chat";

// Use this in-place of "is-typing" for ellipsis as well as input disabling and
// submit button disabling.
export const mostRecentChatIsClient = (chatData: ChatContextData) => {
  const messageHistory = chatData.messageHistory;

  if (messageHistory.length === 0) {
    return false;
  }

  const mostRecentChatItem = messageHistory[messageHistory.length - 1];
  return mostRecentChatItem.originator === "client";
};

export const updateClientData = (
  chatData: ChatContextData,
  setChatData: (chatData: ChatContextData) => void,
  detailsItem: keyof Details,
  value: string | boolean
) => {
  const newClientDetails = {
    ...chatData.originatorDetails["client"],
    [detailsItem]: value,
  };
  const newOriginatorDetails = {
    ...chatData.originatorDetails,
    client: newClientDetails,
  };

  const newChatData = { ...chatData, originatorDetails: newOriginatorDetails };

  setChatData(newChatData);
  return newChatData;
};
