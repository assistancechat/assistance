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

import { GoogleOAuthProvider } from "@react-oauth/google";

import Navbar from "@/components/NavBar";
import ChatModal from "@/components/ChatModal";
import ContactUs from "@/components/ContactUs";
import HeroOpening from "@/components/HeroOpening";
import MoreInfo from "@/components/MoreInfo";

import dataCore from "@/data/general.json";

import {
  ChatContext,
  ChatContextData,
  DefaultChatData,
  MessageHistoryItem,
} from "@/providers/chat";

import { mostRecentChatIsClient } from "@/utilities/flow";
import { callChatApi } from "@/utilities/call-api";

const inter = Inter({ subsets: ["latin"] });

//create a lazy loaded component for the reviews
const Reviews = lazy(() => import("@/components/Reviews"));
const Blog = lazy(() => import("@/components/Blog"));
const Footer = lazy(() => import("@/components/Footer"));

// TODO: Make this type declaration more flexible so that it works for all of
// the page types.
export default function Core(props: { data: typeof dataCore }) {
  const [chatData, setChatData] = useState<ChatContextData>(DefaultChatData);
  const value = { chatData, setChatData };

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
      </Head>
      <GoogleOAuthProvider clientId="332533892028-gmefpu618mrv51k25lhpjtfn09mep8kq.apps.googleusercontent.com">
        <ChatContext.Provider value={value}>
          <Navbar />
          <ChatModal />
          <ContactUs />
          <HeroOpening
            key={props.data.hero.id}
            portraitPicture={props.data.hero.portraitPicture}
            landscapePicture={props.data.hero.landscapePicture}
            alt={props.data.hero.alt}
            courseTitle={props.data.hero.courseTitle}
            headLine1={props.data.hero.headLine1}
            headLine2={props.data.hero.headLine2}
            headLine3={props.data.hero.headLine3}
            headLine4={props.data.hero.headLine4}
            headLine5={props.data.hero.headLine5}
            headLine6={props.data.hero.headLine6}
            subHeading={props.data.hero.subHeading}
            learnButtonText={props.data.hero.learnButtonText}
            learnButtonLink={props.data.hero.learnButtonLink}
            ChatButtonText={props.data.hero.ChatButtonText}
          />
          <MoreInfo
            key={props.data.moreInfo.id}
            heading={props.data.moreInfo.heading}
            subHeading={props.data.moreInfo.subHeading}
            learnButtonText={props.data.moreInfo.learnButtonText}
            learnButtonLink={props.data.moreInfo.learnButtonLink}
            ChatButtonText={props.data.moreInfo.ChatButtonText}
            videoLink={props.data.moreInfo.videoLink}
            videoTitle={props.data.moreInfo.videoTitle}
          />
          <Suspense fallback={<div>Loading...</div>}>
            <Reviews
              key={props.data.reviews.id}
              careerSnapshot={props.data.reviews.careerSnapshot}
              careerSlogan={props.data.reviews.careerSlogan}
              sidePanel={props.data.reviews.sidePanel}
              featured={props.data.reviews.featured}
            />
          </Suspense>
          <Suspense fallback={<div>Loading...</div>}>
            <Blog
              key={props.data.blog.id}
              blogsHeading={props.data.blog.blogsHeading}
              blogsSubHeading={props.data.blog.blogsSubHeading}
              posts={props.data.blog.posts}
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
