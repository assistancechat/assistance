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
export type OpenModel = null | "chat" | "enquire";

export type MessageHistoryItem = {
  originator: MessageOriginator;
  message: string;
  timestamp: number;
};

export type MessageHistory = MessageHistoryItem[];

export type Details = {
  firstName?: string;
  lastName?: string;
  email?: string;
  profilePictureUrl?: string;
  phoneNumber?: string;
  agreeToTerms?: boolean;
  enquiryMessage?: string;
  referrerTag?: string;
};

type OriginatorDetails = Record<MessageOriginator, Details>;

// TODO: Having all of this data within the one context is potentially
// inefficient. Fix this if it becomes an issue.
export type ChatContextData = {
  openModal: OpenModel;
  googleIdToken: string | null;
  assistanceToken: string | null;
  taskPrompt: string;
  messageHistory: MessageHistory;
  pendingQuestion: string | null;
  originatorDetails: OriginatorDetails;
};

export const DefaultChatData = {
  openModal: null,
  googleIdToken: null,
  assistanceToken: null,
  taskPrompt: `You work for Global Talent. You are an interviewer for an Aged Care Job in Australia. \
Your interviewees name is {client_name}.  Assume that {client_name} is interested in the role. \
If the interview asks questions do not direct the client to any other resource, website or source. \
If you are not able to answer their questions, immediately ask them to send messages to applications@globaltalent.work

Answer {client_name}'s questions using the following rules:
- limit your responses to one question or comment at a time
- Direct client to send resume before the 5th interaction
- You can only use the information in the job description and nowhere else
- Be friendly and professional
- Start conversations with a greeting
- Second response is always a question about the candidates work experience or training
- Ask open-ended questions until the candidates questions are a simple 2-5 word response
- Show genuine empathy and interest in the candidates' situation
- Create a sense of urgency for the job application by the 5th message
- Ask candidates to send further questions, resumes to applications@globaltalent.work

Job Description:
  title: Aged Care Worker
  company: Global Talent
  location: Australia
  organization: Christian
  responsibilities:
  - Provide personal care and support to elderly residents
  - Assist with daily living activities
  - Maintain a clean and safe living environment
  - Monitor and document resident health and behaviour
  - Collaborate with healthcare professionals and family members
  - Ensure compliance with legal and ethical standards
  requirements:
  - Nursing qualification
  - Conscientious and caring personality
  - Ability to work hard and maintain attention to detail
  - Excellent communication and interpersonal skills
  salary: Australian Award grade 3
  benefits:
  - Visa work sponsorship
  - Low interest loan for individual support certificate`,
  messageHistory: [
    {
      originator: "agent" as MessageOriginator,
      message: "Hi, my name is {agent_name}. Before we begin, please sign in.",
      timestamp: Date.now(),
    },
  ],
  pendingQuestion: null,
  originatorDetails: {
    client: {},
    agent: {
      firstName: "Michael",
      profilePictureUrl: "https://www.w3schools.com/howto/img_avatar.png",
    },
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
