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

import { useState, useEffect, useContext } from "react";
import { Transition } from "@headlessui/react";
import { PaperAirplaneIcon } from "@heroicons/react/24/outline";

import { ChatContext } from "@/contexts/chat";

import ellipsis from "@/images/ellipsis.svg";

const dateToTimestamp = (date: Date) => {
  const year = date.getFullYear();
  const month = date.getMonth() + 1;
  const day = date.getDate();
  const hour = date.getHours();
  const minute = date.getMinutes();
  const second = date.getSeconds();
  return `${year}-${month}-${day} ${hour}:${minute}:${second}`;
};

function ChatHistory() {
  const { chatData } = useContext(ChatContext);
  const [isTyping, setIsTyping] = useState(false);

  useEffect(() => {
    const messageHistory = chatData.messageHistory;
    const mostRecentChatItem = messageHistory[messageHistory.length - 1];
    setIsTyping(mostRecentChatItem.originator === "user");
  }, [chatData]);

  const renderChatHistory = () => {
    return chatData.messageHistory.map(
      ({ message, originator, timestamp }, index) => {
        const timestampAsString = dateToTimestamp(timestamp);
        const name = chatData.originatorNames[originator];
        const profilePictureUrl =
          chatData.originatorProfilePictureUrls[originator];

        return (
          <div
            key={index}
            className={`flex ${
              originator === "user" ? "justify-end" : "justify-start"
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
                  className={`py-2 px-4 rounded-xl rounded-br-none ${
                    originator === "user"
                      ? "bg-orange-300 text-white"
                      : "bg-gray-800 text-white"
                  } max-w-xs`}
                >
                  {message}
                </div>
                <img
                  className="w-6 h-6 rounded-full -mt-3"
                  src={profilePictureUrl}
                  alt={name}
                />
              </div>
            </div>
          </div>
        );
      }
    );
  };

  return (
    <div className="flex-1 h-full overflow-y-auto">
      <div className="flex flex-col-reverse h-full">
        {renderChatHistory()}
        <Transition
          show={isTyping}
          enter="transition ease-out duration-100"
          enterFrom="transform opacity-0 scale-95"
          enterTo="transform opacity-100 scale-100"
          leave="transition ease-in duration-75"
          leaveFrom="transform opacity-100 scale-100"
          leaveTo="transform opacity-0 scale-95"
        >
          <div className="flex justify-end mb-4">
            <div className="flex flex-col items-end">
              <div className="flex items-center">
                <span className="text-xs text-gray-400 mr-2">...</span>
                <span className="text-xs text-gray-400">user</span>
              </div>
              <div className="flex flex-col items-end">
                <div className="py-2 px-4 rounded-xl rounded-br-none bg-blue-600 text-white max-w-xs">
                  <img src={ellipsis} className="w-4 h-4" alt="ellipsis" />
                </div>
                <img
                  className="w-6 h-6 rounded-full -mt-3"
                  src="https://www.w3schools.com/howto/img_avatar2.png"
                  alt="user"
                />
              </div>
            </div>
          </div>
        </Transition>
      </div>
    </div>
  );
}

function ChatInput({ addNewMessage }) {
  const { setChatData } = useContext(ChatContext);

  const [message, setMessage] = useState("");

  const addNewMessage = (newMessage) => {
    setChatData([...chatData, newMessage]);
  };

  const handleMessageInput = (e) => {
    setMessage(e.target.value);
  };

  const handleMessageSubmit = (e) => {
    e.preventDefault();
    if (message !== "") {
      addNewMessage({
        id: 5,
        name: "user",
        profilepictureurl: "https://www.w3schools.com/howto/img_avatar2.png",
        message: message,
        timestamp: timeStampFunction,
      });
      setMessage("");
    }
  };

  // function that prevents the user from submitting the form if it is empty
  const handleFormSubmit = (e) => {
    e.preventDefault();
  };

  // function that passes a message to the chat history component if the user is typing
  const handleTyping = () => {
    addNewMessage({
      id: 5,
      name: "user",
      profilepictureurl: "https://www.w3schools.com/howto/img_avatar2.png",
      message: "...?...",
      timestamp: timeStampFunction,
    });
  };

  // function that passages a message to the chat history component if the user stops typing after 3 seconds
  const handleTypingTimeout = () => {
    addNewMessage({
      id: 4,
      name: "user",
      profilepictureurl: "https://www.w3schools.com/howto/img_avatar2.png",
      message: "...!...",
      timestamp: "2021-03-01 12:05:00",
    });
  };

  return (
    <div className="flex items-center justify-between p-4 border-t border-gray-200">
      <form className="flex w-full" onSubmit={handleFormSubmit}>
        <div className="flex w-full items-center">
          <input
            type="text"
            className="w-full px-4 py-2 border border-gray-200 rounded-full focus:outline-none focus:border-blue-500"
            placeholder="Type a message..."
            value={message}
            onChange={handleMessageInput}
            onKeyDown={handleTyping}
          />
          <button type="submit" className="ml-4">
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
      <ChatInput />
    </div>
  );
}

export default Chat;
