from conan import ConanFile
from conan.tools.cmake import CMake, cmake_layout
from conan.tools.files import get
from conan.tools.cmake import CMakeToolchain
import os
import subprocess
required_conan_version = ">=1.51.1"


class ModernDurakUnrealCxx(ConanFile):
    name = "modern_durak_unreal_cxx"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    generators = "CMakeDeps"

    def generate(self):
        tc = CMakeToolchain(self)
        tc.user_presets_path = False #workaround because this leads to useless options in cmake-tools configure
        tc.generate()

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        self.options["modern_durak_game"].disable_multiplayer = True
        self.options["modern_durak_game"].ignore_sml_process_event_result_workaround = True

    def requirements(self):
        self.requires("confu_algorithm/2.0.0",force=True)
        self.requires("my_web_socket/2.0.2",transitive_headers=True,force=True)
        self.requires("durak/2.0.0",transitive_headers=True)
        self.requires("boost/1.86.0",force=True,transitive_headers=True)
        self.requires("fmt/11.2.0")
        self.requires("sml/1.1.12",force=True)
        self.requires("confu_json/1.1.1@modern-durak", force=True,transitive_headers=True)
        self.requires("login_matchmaking_game_shared/latest",transitive_headers=True)
        self.requires("modern_durak_game_option/latest",transitive_headers=True)        
        self.requires("modern_durak_game_shared/latest",transitive_headers=True)
        self.requires("matchmaking_proxy/3.0.0",transitive_headers=True)
        self.requires("modern_durak_game/6.2.0",transitive_headers=True)
        self.requires("confu_soci/1.0.0",force=True,transitive_headers=True)

    def source(self):
        token = os.getenv("GIT_TOKEN_MODERN_DURAK_UNREAL_CXX")
        if not token:
            raise Exception("Missing GIT_TOKEN_MODERN_DURAK_UNREAL_CXX environment variable")

        user = "werto87"
        repo_name = "modern_durak_unreal_cxx"
        tag = f"v{self.version}"  # Add 'v' prefix to version
        url = f"https://{token}@github.com/{user}/{repo_name}.git"
        self.output.info(f"Cloning tag '{tag}' from {user}/{repo_name}")
        subprocess.run([
            "git", "clone", "--branch", tag, "--depth", "1", url, "."
        ], check=True)

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def layout(self):
        cmake_layout(self, src_folder=self.name + "-" + str(self.version))

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = [self.name]
        
