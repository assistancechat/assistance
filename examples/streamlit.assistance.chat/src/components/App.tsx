import { component$ } from "@builder.io/qwik";

import Form from "~/components/Form";
import GptChat from "~/components/GptChat";

export default component$(() => {
  return (
    <section
      class={`bg-gradient-to-b md:bg-gradient-to-r from-white via-purple-50 to-sky-100 dark:bg-none mt-[-100px]`}
    >
      <div class="max-w-6xl mx-auto px-4 sm:px-6 md:flex h-screen pt-[100px]">
        <div class="py-12 md:py-12 lg:py-16 block md:flex text-center md:text-left w-full">
          <div class="pb-12 md:pb-0 md:py-0 max-w-5xl mx-auto md:pr-16 flex items-center basis-[30%]">
            <div>
              <h1 class="text-5xl md:text-[3rem] font-bold leading-tighter tracking-tighter mb-4 font-heading px-4 md:px-0">
                Streamlit Assistance Chat
              </h1>
            </div>
          </div>
          <div class="block md:flex items-center flex-1">
            <div class="relative m-auto w-full max-w-lg">
              <div class="pb-5">
                <Form
                  items={[
                    { recordId: "openai-key", formText: "OpenAI API Key" },
                  ]}
                />
              </div>
              <GptChat />
            </div>
          </div>
        </div>
      </div>
    </section>
  );
});
