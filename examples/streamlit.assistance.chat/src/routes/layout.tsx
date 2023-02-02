import { component$, Slot, useClientEffect$ } from "@builder.io/qwik";

export default component$(() => {
  useClientEffect$(() => {
    document.documentElement.classList.remove("dark");
  });

  return (
    <>
      <main>
        <Slot />
      </main>
    </>
  );
});
