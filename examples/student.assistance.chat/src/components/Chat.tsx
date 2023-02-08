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

import {
  useState,
  useContext,
  MouseEvent,
  ChangeEvent,
  FormEvent,
  useEffect,
} from "react";

import { PaperAirplaneIcon } from "@heroicons/react/24/solid";

import jwtDecode from "jwt-decode";
import { GoogleLogin, CredentialResponse } from "@react-oauth/google";

import {
  ChatContext,
  MessageHistoryItem,
  MessageHistory,
} from "@/providers/chat";

import { callChatApi } from "@/utilities/call-chat-api";
import { mostRecentChatIsClient } from "@/utilities/core";

import ProfilePicture from "@/components/atoms/ProfilePicture";

const epochToTimestamp = (epoch: number) => {
  return new Date(epoch).toLocaleString();
};

function ChatHistory() {
  const { chatData } = useContext(ChatContext);

  // Scroll to bottom of chat history when new messages are added
  let messagesEndRef: HTMLDivElement | null = null;
  const scrollToBottom = () => {
    if (messagesEndRef == null) {
      return;
    }

    messagesEndRef.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(scrollToBottom, [chatData.messageHistory]);

  const renderChatHistory = () => {
    return chatData.messageHistory.map(
      ({ message, originator, timestamp }, index) => {
        const timestampAsString = epochToTimestamp(timestamp);
        const name = chatData.originatorDetails[originator].firstName;

        return (
          <div
            key={index}
            className={`flex ${
              originator === "client" ? "justify-end" : "justify-start"
            } mb-4`}
          >
            <div className="flex flex-col items-start p-2">
              <div className="flex items-center">
                <span className="text-xs ml-2 leading-relaxed text-gray-400">
                  {name}
                </span>
              </div>
              <div className="flex flex-col items-end">
                <div
                  className={`py-2 px-4 rounded-xl rounded-br-none ${
                    originator === "client"
                      ? "bg-orange-400 text-white"
                      : "bg-gray-400 text-white"
                  } max-w-xs`}
                >
                  {message
                    .replaceAll(
                      "{agent_name}",
                      chatData.originatorDetails["agent"].firstName
                        ? chatData.originatorDetails["agent"].firstName
                        : "agent"
                    )
                    .replaceAll(
                      "{client_name}",
                      chatData.originatorDetails["client"].firstName
                        ? chatData.originatorDetails["client"].firstName
                        : "client"
                    )}
                </div>
                <ProfilePicture originator={originator} />
              </div>
            </div>
          </div>
        );
      }
    );
  };

  useEffect(() => {
    scrollToBottom();
  }, [chatData.messageHistory]);

  return (
    <div className="flex-1 max-h-96 overflow-scroll">
      <div className="flex flex-col h-full">{renderChatHistory()}</div>
      <div
        ref={(el) => {
          messagesEndRef = el;
        }}
      />
    </div>
  );
}

type GoogleTokenIdData = {
  picture: string;
  given_name: string;
  family_name: string;
  email: string;
};

function Login() {
  const { chatData, setChatData } = useContext(ChatContext);
  const [loginVisible, setLoginVisible] = useState(true);

  const handleCredentialResponse = async (
    credentialResponse: CredentialResponse
  ) => {
    const token = credentialResponse.credential;

    console.log(token);

    if (token == undefined) {
      return;
    }

    const decoded = jwtDecode(token) as GoogleTokenIdData;

    console.log(decoded);

    chatData.originatorDetails["client"].firstName = decoded["given_name"];
    chatData.originatorDetails["client"].lastName = decoded["family_name"];
    chatData.originatorDetails["client"].email = decoded["email"];
    chatData.originatorDetails["client"].profilePictureUrl = decoded["picture"];

    chatData.googleIdToken = token;

    let messageHistoryToAppend: MessageHistory;
    if (chatData.pendingQuestion === null) {
      messageHistoryToAppend = [
        {
          originator: "agent",
          message: `Hi {client_name}, it's great to meet you! Thank you for signing in. How can I help you today?`,
          timestamp: Date.now(),
        },
      ];
    } else {
      messageHistoryToAppend = [
        {
          originator: "agent",
          message: `Hi {client_name}, it's great to meet you! Thank you for signing in.`,
          timestamp: Date.now(),
        },
        {
          originator: "client",
          message: chatData.pendingQuestion,
          timestamp: Date.now(),
        },
      ];

      chatData.pendingQuestion = null;
    }

    const updatedMessageHistory = [
      ...chatData.messageHistory,
      ...messageHistoryToAppend,
    ];

    const updatedChatData = {
      ...chatData,
      messageHistory: updatedMessageHistory,
    };

    setChatData(updatedChatData);

    if (mostRecentChatIsClient(updatedChatData)) {
      await callChatApi(updatedChatData, setChatData);
    }
  };

  useEffect(() => {
    setLoginVisible(chatData.googleIdToken == null);
  }, [chatData]);

  if (loginVisible) {
    return (
      <div className="max-w-xs m-auto pb-6">
        <GoogleLogin
          onSuccess={handleCredentialResponse}
          onError={() => {
            console.log("Login Failed");
          }}
        />
      </div>
    );
  }

  return <></>;
}

function ChatInput() {
  const { chatData, setChatData } = useContext(ChatContext);
  const [message, setMessage] = useState("");

  const addNewMessage = (message: string) => {
    const newMessageHistoryItem: MessageHistoryItem = {
      originator: "client",
      message: message,
      timestamp: Date.now(),
    };

    const updatedMessageHistory = [
      ...chatData.messageHistory,
      newMessageHistoryItem,
    ];

    const updatedChatData = {
      ...chatData,
      messageHistory: updatedMessageHistory,
    };

    setChatData(updatedChatData);
    callChatApi(updatedChatData, setChatData);
  };

  const handleMessageInput = (event: ChangeEvent<HTMLInputElement>) => {
    setMessage(event.target.value);
  };

  const handleMessageSubmit = (event: MouseEvent<HTMLButtonElement>) => {
    event.preventDefault();
    addNewMessage(message);
    setMessage("");
  };

  const preventFormSubmission = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
  };

  return (
    <div className="flex items-center justify-between p-1 border-gray-200">
      <form className="flex w-full" onSubmit={preventFormSubmission}>
        <div className="flex w-full bg-gray-400 items-center rounded-lg">
          <input
            type="text"
            className="w-full px-4 py-2 border border-gray-20000 rounded-l-md focus:outline-none focus:border-orange-600"
            placeholder="Ask us about enrolment or application ..."
            value={message}
            onChange={handleMessageInput}
            disabled={mostRecentChatIsClient(chatData)}
          />
          <button
            type="submit"
            className="bg-orange-400 w-12 justify-center h-full flex rounded-r-lg focus:ring-offset-2 hover:bg-gray-400 focus:ring-white"
            onClick={handleMessageSubmit}
            disabled={message === "" || mostRecentChatIsClient(chatData)}
          >
            <PaperAirplaneIcon className="h-6 w-6 self-center text-white" />
          </button>
        </div>
      </form>
    </div>
  );
}

function Chat() {
  return (
    <div className="flex flex-col flex-1 h-96 bg-gray-800">
      <ChatHistory />
      <Login />
      <ChatInput />
    </div>
  );
}

export default Chat;
