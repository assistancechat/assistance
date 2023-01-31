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
import agentProfilePicture from "@/images/agent-profile-picture.png";
import { StaticImageData } from "next/image";

export type MessageOriginator = "client" | "agent";

export type MessageHistoryItem = {
  originator: MessageOriginator;
  message: string;
  timestamp: number;
};

type MessageHistory = MessageHistoryItem[];

type OriginatorNames = Record<MessageOriginator, string | null>;
type OriginatorProfilePictures = Record<
  MessageOriginator,
  StaticImageData | null
>;

export type ChatContextData = {
  taskPrompt: string;
  messageHistory: MessageHistory;
  originatorNames: OriginatorNames;
  originatorProfilePictures: OriginatorProfilePictures;
};

export const DefaultChatData = {
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
      message:
        "Hi, my name is {agent_name}. Before we begin, may you please sign in",
      timestamp: Date.now(),
    },
  ],
  originatorNames: {
    client: null,
    agent: "Michael",
  },
  originatorProfilePictures: {
    client: null,
    agent: agentProfilePicture,
  },
};

export type ChatContextType = {
  chatData: ChatContextData;
  setChatData: (chatData: ChatContextData) => void;
};

export const ChatContext = createContext<ChatContextType>({
  chatData: DefaultChatData,
  setChatData: (chatData: ChatContextData) => {},
});
