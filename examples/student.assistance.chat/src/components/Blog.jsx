const posts = [
    {
        title: 'Why a Christian Counselling Degree is Unique and Impactful',
        href: '#',
        BlogCategory: {
        name: 'Video',
        href: '#' },
        description:'A Christian Counselling degree is unique in that it combines the best practices of traditional counselling with a biblical perspective. This allows for a holistic approach to helping individuals and families overcome their struggles and find healing. Learn more about the benefits of studying Christian Counselling at Alphacrucis.',
        date: 'January 1, 2022',
        datetime: '2022-01-01T12:00:00',
        imageUrl:'https://images.unsplash.com/photo-1592188657297-c6473609e988?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2487&q=80',
        readingTime: '5 minute read',
        author: {
        name: 'Jane Smith',
        href: '#',
        imageUrl:'https://xsgames.co/randomusers/assets/avatars/female/34.jpg' }
    },
    {
        title: 'Career Opportunities with a Christian Counselling Degree',
        href: '#',
        BlogCategory: {
        name: 'Article',
        href: '#' },
        description:'A Christian Counselling degree can open up a variety of career paths in the helping professions. From working in a church setting to private practice, the options are endless. Learn more about the different career opportunities available with a Christian Counselling degree from Alphacrucis.',
        date: 'February 15, 2022',
        datetime: '2022-02-15T12:00:00',
        imageUrl:'https://images.unsplash.com/photo-1472162314594-eca3c3d90df1?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1738&q=80',
        readingTime: '7 minute video',
        author: {
        name: 'Jesse Doe',
        href: '#',
        imageUrl:'https://xsgames.co/randomusers/assets/avatars/male/31.jpg' }
    },
    {
        title: 'Student Testimonials: Studying Christian Counselling at Alphacrucis',
        href: '#',
        BlogCategory: {
        name: 'Article',
        href: '#' },
        description:'Hear from current and former students about their experiences studying Christian Counselling at Alphacrucis. Learn about the impact the program has had on their personal and professional lives, and why they recommend it to others. Discover what makes Alphacrucis a premier institution for Christian Counselling education.',
        date: 'March 1, 2022',
        datetime: '2022-03-01T12:00:00',
        imageUrl:'https://images.unsplash.com/photo-1523240795612-9a054b0db644?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1740&q=80',
        readingTime: '10 minute read',
        author: {
        name: 'Alphacrucis Student Services',
        href: '#',
        imageUrl:'https://xsgames.co/randomusers/assets/avatars/female/68.jpg' }
    },
  ]

  export default function Blog() {
    return (
      <div className="relative bg-gray-50 px-6 pt-16 pb-20 lg:px-8 lg:pt-24 lg:pb-28">
        <div className="absolute inset-0">
          <div className="h-1/3 bg-white sm:h-2/3" />
        </div>
        <div className="relative mx-auto max-w-7xl">
          <div className="text-center">
            <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl uppercase">Read and inspire</h2>
            <p className="mx-auto mt-3 max-w-2xl text-xl text-gray-500 sm:mt-4 capitalize">
Multiply your talents in faith, study & work            </p>
          </div>
          <div className="mx-auto mt-12 grid max-w-lg gap-5 lg:max-w-none lg:grid-cols-3">
            {posts.map((post) => (
              <div key={post.title} className="flex flex-col overflow-hidden rounded-lg shadow-lg">
                <div className="flex-shrink-0">
                  <img className="h-48 w-full object-cover" src={post.imageUrl} alt="" />
                </div>
                <div className="flex flex-1 flex-col justify-between bg-white p-6">
                  <div className="flex-1">
                    <p className="text-sm font-medium text-indigo-600">
                      <a href={post.BlogCategory.href} className="hover:underline">
                        {post.BlogCategory.name}
                      </a>
                    </p>
                    <a href={post.href} className="mt-2 block">
                      <p className="text-xl font-semibold text-gray-900">{post.title}</p>
                      <p className="mt-3 text-base text-gray-500">{post.description}</p>
                    </a>
                  </div>
                  <div className="mt-6 flex items-center">
                    <div className="flex-shrink-0">
                      <a href={post.author.href}>
                        <span className="sr-only">{post.author.name}</span>
                        <img className="h-10 w-10 rounded-full" src={post.author.imageUrl} alt="" />
                      </a>
                    </div>
                    <div className="ml-3">
                      <p className="text-sm font-medium text-gray-900">
                        <a href={post.author.href} className="hover:underline">
                          {post.author.name}
                        </a>
                      </p>
                      <div className="flex space-x-1 text-sm text-gray-500">
                        <time dateTime={post.datetime}>{post.date}</time>
                        <span aria-hidden="true">&middot;</span>
                        <span>{post.readingTime}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    )
  }
