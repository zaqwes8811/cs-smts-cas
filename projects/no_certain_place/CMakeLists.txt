# FIXME: add ASan and TSan support

# debig troubles
# http://stackoverflow.com/questions/19912648/cmake-qtcreator-mingw-debug-mode-windows-7
# http://www.cmake.org/Wiki/CMake_Useful_Variables
#
# -DCMAKE_BUILD_TYPE=Debug
# -DCMAKE_VERBOSE_MAKEFILE=ON -DCMAKE_C_COMPILER=/usr/bin/clang -DCMAKE_CXX_COMPILER=/usr/bin/clang++
#
# Toolchains:
#   -DCMAKE_TOOLCHAIN_FILE=/home/zaqwes/work/algorithmic-space/platforms/llvm-clang-cilkplus.toolchain.cmake
#
# x64:
#   http://stackoverflow.com/questions/11944060/how-to-detect-target-architecture-using-cmake
#
#
# Intel TBB
#   http://stackoverflow.com/questions/10726537/how-to-install-tbb-from-source-on-linux-and-make-it-work

project(dyn_prog)
cmake_minimum_required(VERSION 2.8)

# conf
set (LCB_USE_TSAN Y)

set(Extern "../../extern/")
set(Intern "../../intern/")
set(GMock "../../extern/gmock-1.6.0/fused-src")
set(Source "source/")
set(testsRoot "./tests")
set(BigExtern "/opt/big-3rdparty/")


# Test framework
include_directories(${GMock})
include_directories(${Source})
include_directories(${Extern}/loki-0.1.7/include)
include_directories(${Extern})
include_directories(${Intern})
include_directories(${BigExtern}/boost_1_57_0)
include_directories(${GMock}/)
include_directories(./src/)
include_directories(${Source}/../../)

EXECUTE_PROCESS( COMMAND uname -m COMMAND tr -d '\n' OUTPUT_VARIABLE ARCHITECTURE )
message( STATUS "Architecture: ${ARCHITECTURE}" )

# link the libraries to the executable
if (UNIX)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

    if(CMAKE_CXX_COMPILER_ID MATCHES "Clang")
        IF(LCB_USE_TSAN)
            set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -O2 -g -fsanitize=thread")
            set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O2 -g -fsanitize=thread")
            set(CMAKE_SHARED_LINKER_FLAGS "${CMAKE_SHARED_LINKER_FLAGS}  -fsanitize=thread")
            set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -fsanitize=thread")
            link_directories(${BigExtern}/boost_1_57_0/clang_tsan_lib64/lib)
            set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -analyse")
        endif()

        link_libraries(
            boost_system boost_thread
            pthread rt)  # !! pthread and rt last!!
    else()
        IF(LCB_USE_TSAN)
            set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -O2 -g -fsanitize=thread -fPIC")
            set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O2 -g -fsanitize=thread -fPIC")

            #set(CMAKE_SHARED_LINKER_FLAGS "${CMAKE_SHARED_LINKER_FLAGS}  -fsanitize=thread")
            set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -fsanitize=thread -pie")
            link_directories(${BigExtern}/boost_1_57_0/gcc_tsan_lib64/lib)
            #link_directories(${BigExtern}/../folly/lib)
        endif()
        link_libraries(
            boost_system boost_thread
            tsan
            #folly
            #glog
            pthread rt)  # !! pthread and rt last!!
    endif()
endif()

message(STATUS "CMAKE_CXX_FLAGS: ${CMAKE_CXX_FLAGS}")

file(GLOB blockedTestSources
    ${testsRoot}/*.cc
    ${testsRoot}/stenf_alg_2/*.cc
    ${Intern}/details/*.cc
)

add_executable(unittest.bin
    ${Source}/mains/launcher_tests.cc
    ${GMock}/gmock-gtest-all.cc
    ${blockedTestSources}
)

