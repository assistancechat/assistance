import Link from 'next/link'
import { Container } from '@/components/Container'

const faqs = [
  [
    {
      question: 'What is AlphaCrucis?',
      answer:
        'AlphaCrucis is an Australian Christian University that provides higher education to students of all backgrounds and beliefs, with a focus on biblical studies and theology.',
    },
    {
      question: 'What programs does AlphaCrucis offer?',
      answer:
        'AlphaCrucis offers a range of undergraduate and graduate programs, including theology, biblical studies, ministry, education, and more. We also offer online and distance learning options for students who are unable to attend on-campus classes.',
    },
    {
      question: 'Can international students enroll at AlphaCrucis?',
      answer:
        'Yes, AlphaCrucis welcomes international students from all countries. However, international students are required to meet certain English language proficiency requirements and obtain a student visa before enrolling in our programs.',
    },
    {
      question: 'What are the admission requirements for AlphaCrucis?',
      answer:
        'The admission requirements for AlphaCrucis vary depending on the program you are applying for. Generally, you will need to provide your academic transcripts, English language proficiency scores (if applicable), and complete an application form. Additional requirements may be necessary for certain programs, such as an interview or portfolio.',
    },
    {
      question: 'What is the tuition cost for AlphaCrucis?',
      answer:
        'The tuition cost for AlphaCrucis varies depending on the program you are enrolled in. International students are generally required to pay higher tuition fees than domestic students. Please visit our website for more information on tuition costs and financial aid options.',
    },
    {
      question: 'How do I apply for enrollment at AlphaCrucis?',
      answer:
        'You can apply for enrollment at AlphaCrucis by submitting an online application on our website. You will be required to provide your academic transcripts, English language proficiency scores (if applicable), and complete an application form. Once your application is received, it will be reviewed by our admissions team and you will be notified of the outcome.',
    },
    {
      question:
        'What kind of support does AlphaCrucis provide for international students?',
      answer:
        'AlphaCrucis provides a range of support services for international students, including assistance with student visas, accommodation, and academic support. We also have a dedicated international student advisor who can provide guidance and support throughout your time at the university.',
    },
    {
      question: 'Is there an age limit for enrolling at AlphaCrucis?',
      answer:
        'There is no age limit for enrolling at AlphaCrucis. We welcome students of all ages who meet the admission requirements for their desired program.',
    },
    {
      question: 'Is there a deadline for enrolling at AlphaCrucis?',
      answer:
        'Yes, there are deadlines for enrolling at AlphaCrucis. These deadlines vary depending on the program you are applying for and the semester you wish to start. It is important to check the deadline for your desired program on our website or contact the admissions office for more information.',
    },
    {
      question: 'What kind of campus facilities does AlphaCrucis have?',
      answer:
        'AlphaCrucis has a range of campus facilities for students to use, including lecture halls, libraries, computer labs, and sports facilities. We also have on-campus accommodation options for students who wish to live on campus.',
    },
    {
      question:
        'Does AlphaCrucis offer any scholarships or financial aid options?',
      answer:
        'Yes, AlphaCrucis offers a range of scholarships and financial aid options for students who are in need of financial assistance. These options include scholarships, bursaries, and student loans. You can find more information on our website or contact the financial aid office for more information.',
    },
  ],
]

export function Faqs() {
  return (
    <section
      id="faqs"
      aria-labelledby="faqs-title"
      className="border-t border-gray-200 py-10 sm:py-32"
    >
      <Container>
        <div className="mx-auto max-w-2xl lg:mx-0">
          <h2
            id="faqs-title"
            className="text-3xl font-medium tracking-tight text-gray-900"
          >
            Frequently Asked Questions
          </h2>
          <p className="mt-2 text-lg text-gray-600">
            If you have anything else you want to ask,{' '}
            <Link
              href="mailto:info@globaltalent.work"
              className="text-gray-900 underline"
            >
              contact us
            </Link>
            .
          </p>
        </div>
        <ul
          role="list"
          className="mx-auto mt-16 grid max-w-2xl grid-cols-1 gap-8 sm:mt-2 lg:max-w-none lg:grid-cols-1"
        >
          {faqs.map((column, columnIndex) => (
            <li key={columnIndex}>
              <ul role="list" className="space-y-10">
                {column.map((faq, faqIndex) => (
                  <li key={faqIndex}>
                    <h3 className="text-lg font-semibold leading-6 text-gray-900">
                      {faq.question}
                    </h3>
                    <p className="mt-4 text-sm text-gray-700">{faq.answer}</p>
                  </li>
                ))}
              </ul>
            </li>
          ))}
        </ul>
      </Container>
    </section>
  )
}
