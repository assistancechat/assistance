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
  googleIdToken: string | null;
  assistanceToken: string | null;
  taskPrompt: string;
  messageHistory: MessageHistory;
  pendingQuestion: string | null;
  originatorNames: OriginatorNames;
  originatorProfilePictureUrls: OriginatorProfilePictureUrls;
};

export const DefaultChatData = {
  open: false,
  googleIdToken: null,
  assistanceToken: null,
  taskPrompt: `You work for Global Talent. You are trying to sell Alphacrucis Courses. \
Your customer's name is {client_name}.  Assume that {client_name} is not able to access \
information from anywhere else except by talking to you. As such, do not redirect them \
to any website or other sources.

Keep in mind the below points in everything you say:

- Personalise with the customer's name
- Clearly communicate course objectives, outcomes, and unique features
- Ask open-ended questions to understand student's needs
- Show genuine empathy and interest in student's situation
- Provide data, testimonials, and case studies for credibility
- Create a sense of urgency for enrolment
- Ensure consistency in messaging, tone, and branding.`,
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
