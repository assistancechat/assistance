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
import { PaperAirplaneIcon } from "@heroicons/react/24/outline";
import jwt_decode from "jwt-decode";
import { GoogleLogin, CredentialResponse } from "@react-oauth/google";

import {
  ChatContext,
  MessageHistoryItem,
  MessageHistory,
  ChatContextData,
} from "@/providers/chat";

import ProfilePicture from "@/components/atoms/ProfilePicture";

const epochToTimestamp = (epoch: number) => {
  return new Date(epoch).toLocaleString();
};

// Use this in-place of "is-typing" for ellipsis as well as input disabling and
// submit button disabling.
const mostRecentChatIsClient = (chatData: ChatContextData) => {
  const messageHistory = chatData.messageHistory;

  if (messageHistory.length === 0) {
    return false;
  }

  const mostRecentChatItem = messageHistory[messageHistory.length - 1];
  return mostRecentChatItem.originator === "client";
};

function ChatHistory() {
  const { chatData } = useContext(ChatContext);

  const renderChatHistory = () => {
    return chatData.messageHistory.map(
      ({ message, originator, timestamp }, index) => {
        const timestampAsString = epochToTimestamp(timestamp);
        const name = chatData.originatorNames[originator];

        return (
          <div
            key={index}
            className={`flex ${
              originator === "client" ? "justify-end" : "justify-start"
            } mb-4`}
          >
            <div className="flex flex-col items-end">
              <div className="flex items-center">
                <span className="text-xs text-gray-400 mr-2">
                  {timestampAsString}
                </span>
                <span className="text-xs text-gray-400">{name}</span>
              </div>
              <div className="flex flex-col items-end">
                <div
                  className={`py-2 px-4 rounded-xl ${
                    originator === "client"
                      ? "bg-orange-300 text-white rounded-br-none"
                      : "bg-gray-800 text-white rounded-bl-none"
                  } max-w-xs`}
                >
                  {message
                    .replaceAll(
                      "{agent_name}",
                      chatData.originatorNames["agent"]
                        ? chatData.originatorNames["agent"]
                        : "agent"
                    )
                    .replaceAll(
                      "{client_name}",
                      chatData.originatorNames["client"]
                        ? chatData.originatorNames["client"]
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

  return (
    <div className="flex-1 h-full overflow-y-auto">
      <div className="flex flex-col h-full">{renderChatHistory()}</div>
    </div>
  );
}

type GoogleTokenIdData = {
  picture: string;
  given_name: string;
};

function Login() {
  const { chatData, setChatData } = useContext(ChatContext);
  const [loginVisible, setLoginVisible] = useState(true);

  const handleCredentialResponse = (credentialResponse: CredentialResponse) => {
    const token = credentialResponse.credential;

    console.log(token);

    if (token == undefined) {
      return;
    }

    const decoded = jwt_decode(token) as GoogleTokenIdData;

    console.log(decoded);

    const profilePictureUrl = decoded["picture"];
    const clientName = decoded["given_name"];

    chatData.originatorNames["client"] = clientName;
    chatData.originatorProfilePictureUrls["client"] = profilePictureUrl;

    chatData.idToken = token;

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

    setChatData({ ...chatData, messageHistory: updatedMessageHistory });
  };

  useEffect(() => {
    setLoginVisible(chatData.idToken == null);
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

    setChatData({ ...chatData, messageHistory: updatedMessageHistory });
  };

  const handleMessageInput = (event: ChangeEvent<HTMLInputElement>) => {
    setMessage(event.target.value);
  };

  const handleMessageSubmit = (event: MouseEvent<HTMLButtonElement>) => {
    event.preventDefault();
    addNewMessage(message);
    setMessage("");
  };

  // Not sure why this is needed.
  const preventFormSubmission = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
  };

  return (
    <div className="flex items-center justify-between p-4 border-t border-gray-200">
      <form className="flex w-full" onSubmit={preventFormSubmission}>
        <div className="flex w-full items-center">
          <input
            type="text"
            className="w-full px-4 py-2 border border-gray-200 rounded-full focus:outline-none focus:border-blue-500"
            placeholder="Type a message..."
            value={message}
            onChange={handleMessageInput}
            // disabled={mostRecentChatIsUser(chatData)}
          />
          <button
            type="submit"
            className="ml-4"
            onClick={handleMessageSubmit}
            // disabled={message === "" || mostRecentChatIsUser(chatData)}
          >
            <PaperAirplaneIcon className="w-6 h-6 text-blue-500" />
          </button>
        </div>
      </form>
    </div>
  );
}

function Chat() {
  return (
    <div className="flex flex-col flex-1 h-full">
      <ChatHistory />
      <Login />
      <ChatInput />
    </div>
  );
}

export default Chat;