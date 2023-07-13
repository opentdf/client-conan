# Conan recipe
OpenTDF recipe for publishing client-cpp to conan repositories

## Process for releasing a new version

In the [client-cpp repo](https://github.com/opentdf/client-cpp):
1. Update the opentdf/client-cpp repository with changes as usual, including updates to CHANGELOG and VERSION as appropriate, and merge to `main`
2. Go to the [releases page](https://github.com/opentdf/client-cpp/releases)
3. Create a new tag and release using the new version number.  Preferred format is N.N.N with no prefix or suffix.
4. Copy the URL for the zipfile of the release under 'Assets'
5. Download the zipfile and get the sha256 (mac/linux: `shasum -a 256 <zip file name>` )

In the [client-conan repo](https://github.com/opentdf/client-conan):
1. Create a release branch from `main`
2. Update the file `recipe/config.yml` and add a new entry for the version 
3. Update the file `recipe/src/conandata.yml` and add a new entry for the version with the URL and sha256 from steps 4 and 5 above
4. Build and test the new version

To build test the recipe locally (substituting the appropriate version number)
`cd <directory containing this README.md>`
Conan 2.0.7:
`conan create --build=opentdf-client --version 1.3.10@ --build=missing recipe/all`

Conan 1.59.0:
`conan create recipe/all opentdf-client/1.3.10@ --build=opentdf-client --build=missing`

To ensure a clean test, run `conan remove opentdf-client` to delete it from conan's cache and delete the `recipe/all/test_package/build` directory to remove stale test package build artifacts.

Do not check in the `all/test_package/build` directory, ignore or delete it before submitting changes

5. Merge the release branch into `main`
6. Publish to conan per instructions (see below)


## Building with this recipe instead of CCI published recipe

## Building an unreleased client-cpp branch using a local clone of this recipe

You can specify branch-version to pull source from a client-cpp branch instead of a tagged version in the conandata.yml file.  Once it is built and in the local conan cache,
you can consume it in other project conanfile.py self.requires lists.
Make a local clone of this repo, and from the root issue:

NOTE: branch names must be all lowercase due to a conan restriction

conan 2.0.7

`git clean -ffdx;rm -rf ~/.conan2/p/b/opent*;rm -rf ~/.conan2/p/t/opent*;rm -rf ~/.conan2/p/opent*;conan remove opentdf-client`
`conan create --build=opentdf-client --build=missing recipe/all --version plat-1649-conan2-compatability -o opentdf-client/\*:branch_version=True`

conan 1.59.0

`git clean -ffdx;rm -rf ~/.conan/data/opentdf-client/plat-1649-conan2-compatability;conan remove opentdf-client`
`conan create recipe/all opentdf-client/PLAT-1649-conan2-compatability@ --build=opentdf-client --build=missing -o opentdf-client:branch_version=True`

## Publishing to a conan repository

### conan-center repository:
There are two cases to consider when publishing to conan-center.  

The simplest case is when the only change needed to the recipe is to add a checksum and tag for a new release on client-cpp.  There is a bot that runs on conan-center that scans the repos looking for new releases.  If it finds one, a link is generated that will create an update PR for you.  This generated PR will be processed by automation, and can be completed and published in under an hour.

The more complex case is when anything other than just the version and checksum is being changed.  This requires a PR to be created and submitted manually, followed by a manual review process.  This can take several weeks.

Please keep the content of client-conan in sync with the recipe published at conan-center

#### Automated version bump PR process

Using the Updatable Recipes bot documented at conan-center [here](https://github.com/conan-io/conan-center-index/blob/master/docs/community_resources.md)
1. Go to the Updatable Recipes results list and find the opentdf-client entry
2. Click on the 'open one' link to create a PR
3. Finish filling out the PR description, and submit it

#### Manual PR process

Documentation for publishing to conan-center is [here](https://github.com/conan-io/conan-center-index/blob/master/docs/how_to_add_packages.md)

Create a PR to update the materials in the `opentdf-client` recipe in the index.  The PR will be merged into the conan-center master index when it has 3 approvals.  The approvals are manual, and completed by volunteer staff at conan-center.  This can take several weeks.
