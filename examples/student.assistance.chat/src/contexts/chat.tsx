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

type MessageOriginator = "user" | "agent";

type MessageHistoryItem = {
  originator: MessageOriginator;
  message: string;
  timestamp: Date;
};

type MessageHistory = MessageHistoryItem[];

type OriginatorNames = Record<MessageOriginator, string>;
type OriginatorProfilePictureUrls = Record<MessageOriginator, string>;

export type ChatContextData = {
  messageHistory: MessageHistory;
  originatorNames: OriginatorNames;
  originatorProfilePictureUrls: OriginatorProfilePictureUrls;
};

export const DefaultChatData = {
  messageHistory: [],
  originatorNames: {
    user: "user",
    agent: "George Paul Thompson",
  },
  originatorProfilePictureUrls: {
    user: "https://www.w3schools.com/howto/img_avatar2.png",
    agent: "https://www.w3schools.com/howto/img_avatar.png",
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
