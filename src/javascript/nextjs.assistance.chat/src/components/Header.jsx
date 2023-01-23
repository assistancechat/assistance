import Link from 'next/link'
import { Logo2 } from '@/components/Logo'
import { Container } from '@/components/Container'

export function Header() {
  return (
    <header>
      <nav>
        <Container className="relative z-50 flex justify-between py-8">
          <div className="relative z-10 flex items-center gap-16">

            <div className="flex items-center text-gray-900">
              <Link href="/" aria-label="Home"><Logo2 className="flex-none w-20 fill-cyan-500" /></Link>
              <div className="ml-4">
                <p className="text-base font-semibold">Student Assistance Chat</p>
                <p className="mt-1 text-sm">Easy, Fast & Stress Free Answers to your Questions</p>
              </div>
            </div>
          </div>
        </Container>
      </nav>
    </header>
  )
}
