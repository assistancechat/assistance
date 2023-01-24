python_sources(name="lib", sources=["**/*.py"])

python_distribution(
    name="assistance-packaged",
    dependencies=[
        ":lib",
        ":resources",
    ],
    sdist=True,
    wheel=True,
    provides=python_artifact(
        name="assistance",
    ),
    generate_setup=False,
)

resources(
    name="resources",
    sources=[
        "LICENSE",
        "README.md",
        "pyproject.toml",
        "assistance/py.typed",
    ],
)
