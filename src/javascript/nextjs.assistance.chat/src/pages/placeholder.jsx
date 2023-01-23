import Head from 'next/head'
import {useRef} from 'react'
import { CallToAction } from '@/components/CallToAction'
import { Faqs } from '@/components/Faqs'
import { Footer } from '@/components/Footer'
import { Header } from '@/components/Header'
import { Hero } from '@/components/Hero'
import { HowItWorks } from '@/components/HowItWorks'
import { Reviews } from '@/components/Reviews'
import { useInView } from "framer-motion";
import React from 'react'

function Section({ children }) {
  const ref = useRef(null);
  const isInView = useInView(ref, { once: false });

  return (
    <section ref={ref}>
      <span
        style={{
          transform: isInView ? "none" : "translateX(-200px)",
          opacity: isInView ? 1 : 0,
          transition: "all 0.4s cubic-bezier(0.17, 0.55, 0.55, 1) 0.3s"
        }}
      >
        {children}
      </span>
    </section>
  );
}


export default function Home() {
  return (
    <>
      <Head>
        <title>Enroll effortlessly, talk to our team and let us do the rest</title>
        <meta name="keywords" content="Alphacrucis, university, enrolment, students, program of study, campus location, automated enrolment process, convenient, accurate, stress-free" />
        <meta name="description" content="Easily enroll in Alphacrucis University with our innovative automated enrolment process. Simply talk to our team and let us fill out your enrolment form for you, ensuring all information is accurate and up-to-date. Convenient, accurate, and stress-free enrolment for students of all programs and campus locations." />
      </Head>
      <Header />
      <main>

      <Section><Hero /></Section>
        <Section><HowItWorks /> </Section>
        <Section><Reviews /></Section>
        <Section><CallToAction /></Section>
        <Section><Faqs /></Section>
      </main>
      <Footer />
    </>
  )
}
