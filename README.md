# Conan recipe
Recipe for publishing to conan repositories

## Process for releasing a new version

In the client-cpp repo:
1. Update the opentdf/client-cpp repository with changes as usual, including updates to CHANGELOG and VERSION as appropriate, and merge to `main`
2. Go to the [releases page](https://github.com/opentdf/client-cpp/releases)
3. Create a new tag and release using the new version number
4. Copy the URL for the zipfile of the release under 'Assets'
5. Download the zipfile and get the sha256 (mac/linux: `shasum -a 256 <zip file name>` )

In the client-conan repo:
1. Create a release branch from `main`
2. Update the file `recipe/config.yml` and add a new entry for the version 
3. Update the file `recipe/src/conandata.yml` and add a new entry for the version with the URL and sha256 from steps 4 and 5 above
4. Merge the release branch into `main`
5. Publish to conan per instructions (see below)

## Publishing to a conan repository

### conan-center:

Create a PR to update the materials in the `opentdf-client` recipe in the index.  The PR will be merged into the conan-center master index when it is approved.

Documentation for publishing to conan-center is [here](https://github.com/conan-io/conan-center-index/blob/master/docs/how_to_add_packages.md)

To test the recipe locally
`cd <directory containing this README.md>`
`conan create recipe/all opentdf-client/0.2.4@ -pr:b=default --build=opentdf-client`

To ensure a clean test, run `conan remove opentdf-client` to delete it from conan's cache and delete the `recipe/all/test_package/build` directory to remove stale test package build artifacts.

Do not check in the `all/test_package/build` directory, ignore or delete it before submitting changes

### Nexus:

`conan upload virtru-nexus opentdf-client`

