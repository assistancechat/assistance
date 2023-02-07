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

import { useContext, Fragment } from "react";
import { Dialog, Transition } from "@headlessui/react";
import { XMarkIcon } from "@heroicons/react/24/outline";

import { ChatContext } from "@/providers/chat";

import Chat from "@/components/Chat";

function ChatModal() {
  const { chatData, setChatData } = useContext(ChatContext);

  const closeModal = () => {
    setChatData({ ...chatData, openModel: null });
  };

  return (
    <Transition appear show={chatData.openModel === "chat"} as={Fragment}>
      <Dialog
        as="div"
        className="fixed inset-0 z-10 overflow-y-auto"
        onClose={closeModal}
      >
        <Transition.Child
          as={Fragment}
          enter="ease-out duration-300"
          enterFrom="opacity-0"
          enterTo="opacity-100"
          leave="ease-in duration-200"
          leaveFrom="opacity-100"
          leaveTo="opacity-0"
        >
          <div className="fixed inset-0 bg-black bg-opacity-25" />
        </Transition.Child>
        <div className="fixed inset-0 overflow-y-auto">
          <div className="flex min-h-full items-center justify-center p-2 text-center">
            <Transition.Child
              as={Fragment}
              enter="ease-out duration-300"
              enterFrom="opacity-0 scale-95"
              enterTo="opacity-100 scale-100"
              leave="ease-in duration-200"
              leaveFrom="opacity-100 scale-100"
              leaveTo="opacity-0 scale-95"
            >
              <Dialog.Panel className="w-full rounded max-w-2xl transform bg-gray-800 overflow-visible mb-2 p-2 text-left align-middle shadow-5xl transition-all">
                <div className="flex justify-end">
                  <button>
                    <XMarkIcon
                      className="h-6 w-6 text-gray-500 rounded border border-gray-500 hover:bg-white focus:outline-none focus:ring-2 focus:ring-white focus:text-orange-200 sfocus:ring-offset-2"
                      aria-hidden="true"
                      onClick={closeModal}
                    />
                  </button>
                </div>
                <Chat />
              </Dialog.Panel>
            </Transition.Child>
          </div>
        </div>{" "}
      </Dialog>
    </Transition>
  );
}

export default ChatModal;
