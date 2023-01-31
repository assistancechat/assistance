import { useEffect, useState, lazy, Suspense } from "react";

import sha224 from "crypto-js/sha224";

import Head from "next/head";
import { Inter } from "@next/font/google";

import { GoogleOAuthProvider } from "@react-oauth/google";

import Navbar from "@/components/NavBar";
import Hero from "@/components/Hero";
import MoreInfo from "@/components/MoreInfo";
import StudentExperience from "@/components/StudentExperience";
import Blog from "@/components/Blog";
import Footer from "@/components/Footer";

import { ChatContext, ChatContextData, DefaultChatData } from "@/contexts/chat";

const inter = Inter({ subsets: ["latin"] });

//create a lazy loaded component for the reviews
const Reviews = lazy(() => import("@/components/Reviews"));

export default function Home() {
  // Details on implementation https://stackoverflow.com/a/51573816/3912576
  const [chatData, setChatData] = useState<ChatContextData>(DefaultChatData);
  const value = { chatData, setChatData };

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
          <Hero />
          <MoreInfo />
          <Suspense fallback={<div>Loading...</div>}>
            <Reviews />
          </Suspense>
          <StudentExperience />
          <Blog />
          <Footer />
        </ChatContext.Provider>
      </GoogleOAuthProvider>
      ;
    </>
  );
}
