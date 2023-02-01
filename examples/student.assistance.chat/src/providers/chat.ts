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

import { createContext } from "react";

export type MessageOriginator = "client" | "agent";

export type MessageHistoryItem = {
  originator: MessageOriginator;
  message: string;
  timestamp: number;
};

export type MessageHistory = MessageHistoryItem[];

type OriginatorNames = Record<MessageOriginator, string | null>;
type OriginatorProfilePictureUrls = Record<MessageOriginator, string | null>;

// TODO: Having all of this data within the one context is potentially
// inefficient. Fix this if it becomes an issue.
export type ChatContextData = {
  open: boolean;
  idToken: string | null;
  taskPrompt: string;
  messageHistory: MessageHistory;
  pendingQuestion: string | null;
  originatorNames: OriginatorNames;
  originatorProfilePictureUrls: OriginatorProfilePictureUrls;
};

export const DefaultChatData = {
  open: false,
  idToken: null,
  taskPrompt: `You are from Assistance.Chat. You are an expert in all things \
about Alphacrucis (AC) Christian University. You are providing \
student support to {client_name}.

If relevant, it is your goal to sell an AC course to \
{client_name}.

You are always polite and helpful. Even when talked to \
inappropriately by {client_name}.

Assume that {client_name} is not able to access information \
from anywhere else except by talking to you. As such, do not \
redirect them to any website or other sources.`,
  messageHistory: [
    {
      originator: "agent" as MessageOriginator,
      message: "Hi, my name is {agent_name}. Before we begin, please sign in.",
      timestamp: Date.now(),
    },
  ],
  pendingQuestion: null,
  originatorNames: {
    client: null,
    agent: "Michael",
  },
  originatorProfilePictureUrls: {
    client: null,
    agent: "https://www.w3schools.com/howto/img_avatar.png",
  },
};

export type ChatContextType = {
  chatData: ChatContextData;
  setChatData: (chatData: ChatContextData) => void;
};

// TODO: A provider like this would be helpful within a @assistance.chat/react
// package. Once we spin up a second website it would be worth moving all of
// the common code out into a library.
export const ChatContext = createContext<ChatContextType>({
  chatData: DefaultChatData,
  setChatData: (chatData: ChatContextData) => {},
});
