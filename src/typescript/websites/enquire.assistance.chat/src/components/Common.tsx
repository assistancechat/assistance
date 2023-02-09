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

import { useState, useEffect } from "react";

import Head from "next/head";
import { Inter } from "@next/font/google";
import { useRouter } from "next/router";

import { GoogleOAuthProvider } from "@react-oauth/google";

import ContactUsModal from "@/components/ContactUsModal";

import {
  ChatContext,
  ChatContextData,
  DefaultChatData,
} from "@/providers/chat";

import { updateClientData } from "@/utilities/core";

const inter = Inter({ subsets: ["latin"] });

export default function Common() {
  const [chatData, setChatData] = useState<ChatContextData>(DefaultChatData);
  const value = { chatData, setChatData };

  const router = useRouter();
  const tag = router.query.tag;

  const removeQueryParam = (param: string) => {
    const { pathname, query } = router;
    const params = new URLSearchParams(query as any);
    params.delete(param);
    router.replace({ pathname, query: params.toString() }, undefined, {
      shallow: true,
    });
  };

  useEffect(() => {
    if (tag != null) {
      // TODO: Consider handling the case where tag might be string[].
      updateClientData(chatData, setChatData, "referrerTag", tag as string);
      removeQueryParam("tag");
      console.log("tag:", tag);
    }
  }, [tag]);

  return (
    <>
      <Head>
        <title>Global Talent</title>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <GoogleOAuthProvider clientId="332533892028-gmefpu618mrv51k25lhpjtfn09mep8kq.apps.googleusercontent.com">
        <ChatContext.Provider value={value}>
          <ContactUsModal />
        </ChatContext.Provider>
      </GoogleOAuthProvider>
      ;
    </>
  );
}
