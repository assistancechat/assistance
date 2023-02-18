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

import { useState, lazy, Suspense, useEffect } from "react";

import Head from "next/head";
import { Inter } from "@next/font/google";
import { useRouter } from "next/router";

import { GoogleOAuthProvider } from "@react-oauth/google";

import Navbar from "@/components/NavBar";
import ChatModal from "@/components/ChatModal";
import ContactUsModal from "@/components/ContactUsModal";
import HeroOpening from "@/components/Hero";
import MoreInfo from "@/components/MoreInfo";
import TikTokAnalytics from "@/components/TikTokAnalytics";
import data from "@/data/agedCare.json";

import {
  ChatContext,
  ChatContextData,
  DefaultChatData,
  MessageHistoryItem,
} from "@/providers/chat";

import { mostRecentChatIsClient, updateClientData } from "@/utilities/core";
import { callChatApi } from "@/utilities/call-chat-api";

const inter = Inter({ subsets: ["latin"] });

//create a lazy loaded component for the reviews
const Reviews = lazy(() => import("@/components/Reviews"));
const Blog = lazy(() => import("@/components/Blog"));
const Footer = lazy(() => import("@/components/Footer"));
const AboutUs = lazy(() => import("@/components/AboutUs"));

// TODO: Make this type declaration more flexible so that it works for all of
// the page types.
export default function AgedCare() {

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

  useEffect(() => {
    const appendPendingQuestionIfReady = async () => {
      if (chatData.googleIdToken == null) {
        return;
      }

      if (mostRecentChatIsClient(chatData)) {
        return;
      }

      if (!chatData.pendingQuestion) {
        return;
      }

      const messageHistoryToAppend: MessageHistoryItem = {
        originator: "client",
        message: chatData.pendingQuestion,
        timestamp: Date.now(),
      };

      const updatedMessageHistory = [
        ...chatData.messageHistory,
        messageHistoryToAppend,
      ];

      const updatedChatData = {
        ...chatData,
        messageHistory: updatedMessageHistory,
        pendingQuestion: null,
      };

      setChatData(updatedChatData);
      await callChatApi(updatedChatData, setChatData);
    };

    appendPendingQuestionIfReady();
  }, [chatData]);
  
  return (
    <>
      <Head>
        <title>Global Talent</title>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
        <TikTokAnalytics />
      </Head>
      <GoogleOAuthProvider clientId="332533892028-gmefpu618mrv51k25lhpjtfn09mep8kq.apps.googleusercontent.com">
        <ChatContext.Provider value={value}>
          <Navbar />
          <ChatModal />
          <ContactUsModal />
          <HeroOpening
            key={data.hero.id}
            portraitPicture={data.hero.portraitPicture}
            landscapePicture={data.hero.landscapePicture}
            alt={data.hero.alt}
            chatButtonText={data.hero.chatButtonText}
          />
          <Suspense fallback={<div>Loading...</div>}>
            <Reviews
              careerSnapshot={data.reviews.careerSnapshot}
              careerSlogan={data.reviews.careerSlogan}
              sidePanels={data.reviews.sidePanels}
              featured={data.reviews.featured}
            />
          </Suspense>
          <Suspense fallback={<div>Loading...</div>}>
          <AboutUs />
          </Suspense>
          <Suspense fallback={<div>Loading...</div>}>
            <Blog
              id={data.blog.id}
              blogHeading={data.blog.blogsHeading}
              blogSubHeading={data.blog.blogsSubHeading}
              posts={data.blog.posts}
            />
          </Suspense>
          <Suspense fallback={<div>Loading...</div>}>
            <Footer />
          </Suspense>

        </ChatContext.Provider>
      </GoogleOAuthProvider>
      ;
    </>
  );
}


