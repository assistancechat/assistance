import { component$, Slot } from '@builder.io/qwik';
import Chat from "../components/chat/chat";

export default component$(() => {
  return (
    <>
      <main>
          <Slot />
          <Chat />
      </main>
    </>
  );
});
