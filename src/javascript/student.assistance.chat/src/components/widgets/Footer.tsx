import { component$ } from "@builder.io/qwik";
import { Link } from "@builder.io/qwik-city";

import { IconTwitter } from "~/components/icons/IconTwitter";
import { IconLinkedIn } from "~/components/icons/IconLinkedIn";
import { IconGithub } from "~/components/icons/IconGithub";

export default component$(() => {
  const social = [
    { label: "LinkedIn", icon: IconLinkedIn, href: "https://www.linkedin.com/company/OpenSaMD/" },
    { label: "Twitter", icon: IconTwitter, href: "https://twitter.com/OpenSaMD" },
    {
      label: "Github",
      icon: IconGithub,
      href: "https://github.com/OpenSaMD/OpenSaMD",
    },
  ];

  return (
    <footer class="border-t border-gray-200 dark:border-slate-800">
      <div class="max-w-6xl mx-auto px-4 sm:px-6">

        <div class="md:flex md:items-center md:justify-between py-6 md:py-8">
          <ul class="flex mb-4 md:order-1 -ml-2 md:ml-4 md:mb-0">
            {social.map(({ label, href, icon: Icon }) => (
              <li>
                <Link
                  class="text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 focus:outline-none focus:ring-4 focus:ring-gray-200 dark:focus:ring-gray-700 rounded-lg text-sm p-2.5 inline-flex items-center"
                  aria-label={label}
                  title={label}
                  href={href}
                >
                  {Icon && <Icon />}
                </Link>
              </li>
            ))}
          </ul>

          <div class="text-sm text-gray-700 mr-4 dark:text-slate-400">

          </div>
        </div>
      </div>
    </footer>
  );
});
