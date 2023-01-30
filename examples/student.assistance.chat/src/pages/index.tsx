import { useState, lazy, Suspense } from "react";
import Head from "next/head";
import { Inter } from "@next/font/google";
import Navbar from "@/components/NavBar";
import Hero from "@/components/Hero";
import MoreInfo from "@/components/MoreInfo";
import StudentExperience from "@/components/StudentExperience";
import Blog from "@/components/Blog";
import Footer from "@/components/Footer";


const inter = Inter({ subsets: ["latin"] });

//create a lazy loaded component for the reviews
const Reviews = lazy(() => import("@/components/Reviews"));

export default function Home() {

  return (

    <>
      <Head>
        <title>Global Talent</title>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <Navbar />
      <Hero />
      <MoreInfo />
      <Suspense fallback={<div>Loading...</div>}>
      <Reviews />
      </Suspense>
      <StudentExperience />
      <Blog />
      <Footer />

    </>
  );
}