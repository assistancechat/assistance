export default function fourohfour() {
    return (
      <>
        <main
          className="h-screen w-screen bg-cover bg-top sm:bg-top"
          style={{
            backgroundImage:
              'url("https://images.unsplash.com/photo-1504275107627-0c2ba7a43dba?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1548&q=80")',
          }}
        >
          <div>
          <div className=" mt-20 flex place-self-center flex-col mx-auto max-w-7xl py-16 bg-orange-500 bg-opacity-80 px-6 text-center sm:py-24 lg:px-8 lg:py-48">
            <p className="text-5xl font-semibold text-black ">404</p>
            <h1 className="mt-2 text-3xl font-bold tracking-tight text-white sm:text-5xl">Uh Oh! I think you’re lost.</h1>
            <p className="mt-2 text-3xl font-medium text-white">
              It looks like the page you{"’"}re looking for doesn{"'"}t exist.
            </p>
            <div className="mt-6">
              <a
                href="#Home"
                className="inline-flex items-center rounded-md border border-transparent bg-white bg-opacity-75 px-4 py-2 text-3xl font-medium text-white text-opacity-75 sm:bg-opacity-25 sm:hover:bg-opacity-50"
              >
                Go back home
              </a>
            </div>
          </div>
          </div>
        </main>
      </>
    )
  }
  