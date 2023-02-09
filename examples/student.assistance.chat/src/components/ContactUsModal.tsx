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

import { useContext, Fragment, useState, useEffect, FormEvent } from "react";
import { Dialog, Transition, Switch } from "@headlessui/react";

import { ChatContext, ChatContextData, Details } from "@/providers/chat";
import { updateClientData } from "@/utilities/core";
import { EnvelopeIcon } from "@heroicons/react/24/solid";
import { callContactUsApi } from "@/utilities/call-contact-us-api";
import { FormThankYou } from "@/components/FormThankYou";

function ContactUs() {
  const { chatData, setChatData } = useContext(ChatContext);

  const [agreed, setAgreed] = useState(false);
  const [allDataFilledOut, setAllDataFilledOut] = useState(false);
  const [showThankYou, setShowThankYou] = useState(false);

  const onChange = (e: any, detailsItem: keyof Details) => {
    updateClientData(chatData, setChatData, detailsItem, e.target.value);
  };

  useEffect(() => {
    updateClientData(chatData, setChatData, "agreeToTerms", agreed);
  }, [agreed]);

  useEffect(() => {
    setAllDataFilledOut(determineIfAllDataFilledOut());
  }, [chatData]);

  function classNames(...classes: string[]) {
    return classes.filter(Boolean).join(" ");
  }

  const determineIfAllDataFilledOut = () => {
    const clientDetails = chatData.originatorDetails["client"];
    return (
      isFilledOut(clientDetails.firstName) &&
      isFilledOut(clientDetails.lastName) &&
      isFilledOut(clientDetails.email) &&
      isFilledOut(clientDetails.phoneNumber) &&
      isFilledOut(clientDetails.enquiryMessage) &&
      clientDetails.agreeToTerms === true
    );
  };

  const isFilledOut = (value: string | null | undefined) => {
    return value != null && value !== "";
  };

  const closeModal = (chatData: ChatContextData) => {
    setChatData({ ...chatData, openModal: null });
  };

  const formSubmission = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    await callContactUsApi(chatData);

    const newChatData = updateClientData(
      chatData,
      setChatData,
      "enquiryMessage",
      ""
    );
    closeModal(newChatData);

    setShowThankYou(true);
  };

  return (
    <>
      <Transition appear show={chatData.openModal === "enquire"} as={Fragment}>
        <Dialog
          as="div"
          className="relative z-10 "
          onClose={() => {
            closeModal(chatData);
          }}
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
            <div className="flex min-h-full items-center justify-center p-4 text-center">
              <Transition.Child
                as={Fragment}
                enter="ease-out duration-300"
                enterFrom="opacity-0 scale-95"
                enterTo="opacity-100 scale-100"
                leave="ease-in duration-200"
                leaveFrom="opacity-100 scale-100"
                leaveTo="opacity-0 scale-95"
              >
                <Dialog.Panel className="w-full max-w-md transform overflow-hidden rounded-2xl bg-gray-800 p-6 text-left align-middle shadow-xl transition-all">
                  <Dialog.Title
                    as="h3"
                    className="text-3xl font-medium inline-flex leading-none text-white space-x-1"
                  >
                    <EnvelopeIcon className="text-orange-400 w-8 animate-pulse" />
                    <h1>Contact Us</h1>
                  </Dialog.Title>
                  <div className="mt-5">
                    <form
                      action="#"
                      method="POST"
                      className="grid grid-cols-1 gap-y-6 sm:grid-cols-2 sm:gap-x-8"
                      onSubmit={formSubmission}
                    >
                      <div>
                        <label
                          htmlFor="first-name"
                          className="block text-sm font-medium text-orange-400"
                        >
                          First name
                        </label>
                        <div className="mt-1">
                          <input
                            type="text"
                            name="first-name"
                            id="first-name"
                            value={
                              chatData.originatorDetails["client"][
                                "firstName"
                              ] || ""
                            }
                            onChange={(e) => onChange(e, "firstName")}
                            autoComplete="given-name"
                            className="block w-full rounded-md border-gray-300 py-3 px-4 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                          />
                        </div>
                      </div>
                      <div>
                        <label
                          htmlFor="last-name"
                          className="block text-sm font-medium text-orange-400"
                        >
                          Last name
                        </label>
                        <div className="mt-1">
                          <input
                            type="text"
                            name="last-name"
                            id="last-name"
                            value={
                              chatData.originatorDetails["client"][
                                "lastName"
                              ] || ""
                            }
                            onChange={(e) => onChange(e, "lastName")}
                            autoComplete="family-name"
                            className="block w-full rounded-md border-gray-300 py-3 px-4 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                          />
                        </div>
                      </div>
                      <div className="sm:col-span-2">
                        <label
                          htmlFor="email"
                          className="block text-sm font-medium text-orange-400"
                        >
                          Email
                        </label>
                        <div className="mt-1">
                          <input
                            id="email"
                            name="email"
                            type="email"
                            value={
                              chatData.originatorDetails["client"]["email"] ||
                              ""
                            }
                            onChange={(e) => onChange(e, "email")}
                            autoComplete="email"
                            className="block w-full rounded-md border-gray-300 py-3 px-4 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                          />
                        </div>
                      </div>
                      <div className="sm:col-span-2">
                        <label
                          htmlFor="phone-number"
                          className="block text-sm font-medium text-orange-400"
                        >
                          Phone Number
                        </label>
                        <div className="relative mt-1 rounded-md shadow-sm">
                          <input
                            type="text"
                            name="phone-number"
                            id="phone-number"
                            value={
                              chatData.originatorDetails["client"][
                                "phoneNumber"
                              ] || ""
                            }
                            onChange={(e) => onChange(e, "phoneNumber")}
                            autoComplete="tel"
                            className="block w-full rounded-md border-gray-300 py-3 px-4  focus:border-indigo-500 focus:ring-indigo-500"
                            placeholder="+61 1234 5678"
                          />
                        </div>
                      </div>
                      <div className="sm:col-span-2">
                        <label
                          htmlFor="message"
                          className="block text-sm font-medium text-orange-400"
                        >
                          Message
                        </label>
                        <div className="mt-1">
                          <textarea
                            id="message"
                            name="message"
                            value={
                              chatData.originatorDetails["client"][
                                "enquiryMessage"
                              ] || ""
                            }
                            onChange={(e) => onChange(e, "enquiryMessage")}
                            rows={4}
                            className="block w-full rounded-md border-gray-300 py-3 px-4 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                          />
                        </div>
                      </div>
                      <div className="sm:col-span-2">
                        <div className="flex items-start">
                          <div className="flex-shrink-0">
                            <Switch
                              checked={agreed}
                              onChange={setAgreed}
                              className={classNames(
                                agreed ? "bg-indigo-600" : "bg-gray-200",
                                "relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
                              )}
                            >
                              <span className="sr-only">Agree to policies</span>
                              <span
                                aria-hidden="true"
                                className={classNames(
                                  agreed ? "translate-x-5" : "translate-x-0",
                                  "inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out"
                                )}
                              />
                            </Switch>
                          </div>
                          <div className="ml-3">
                            <p className="text-base text-gray-500">
                              By selecting this, you agree to the{" "}
                              <a
                                href="#"
                                className="font-medium text-orange-400 underline"
                              >
                                Privacy Policy
                              </a>{" "}
                              and{" "}
                              <a
                                href="#"
                                className="font-medium text-orange-400 underline"
                              >
                                Cookie Policy
                              </a>
                              .
                            </p>
                          </div>
                        </div>
                      </div>
                      <div className="sm:col-span-2">
                        <button
                          type="submit"
                          disabled={!allDataFilledOut}
                          className={classNames(
                            allDataFilledOut
                              ? " bg-indigo-600  hover:bg-indigo-700"
                              : " bg-gray-600",
                            "inline-flex w-full items-center justify-center rounded-md border border-transparent px-6 py-3 text-base font-medium text-white shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
                          )}
                        >
                          Let's talk
                        </button>
                      </div>
                    </form>
                  </div>
                </Dialog.Panel>
              </Transition.Child>
            </div>
          </div>
        </Dialog>
      </Transition>
      <FormThankYou
        show={showThankYou}
        setShow={setShowThankYou as (show: boolean) => {}}
      />
    </>
  );
}

export default ContactUs;
