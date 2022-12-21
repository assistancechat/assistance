import { component$, Slot } from '@builder.io/qwik';
import Chat from "../components/chat/chat";

export default component$(() => {
  return (
    <>
      <main>
          <Slot />
          <Chat conversation={
            [
              "Hi there! Can you tell me a little about yourself and what your skills and interests are?",
              "Lorem ipsum dolor, sit amet consectetur adipisicing elit. Magnam, repudiandae."
            ]
          } />
      </main>
    </>
  );
});
