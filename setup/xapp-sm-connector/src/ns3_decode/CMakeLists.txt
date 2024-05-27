set ( major_version "1" )
set ( minor_version "0" )
set ( patch_level "0" )
set( install_inc "include/proto" )
if( NOT CMAKE_INSTALL_LIBDIR )
	set( CMAKE_INSTALL_LIBDIR "lib" )
endif()

set( install_lib "${CMAKE_INSTALL_LIBDIR}" )
#

file(GLOB SOURCES "*.cc")
file(GLOB HEADERS "*.h")
# file(GLOB PROTOBUF_FILELIST "*.proto")
set(PROTOBUF_FILELIST sl-mac-pdu-tag.proto sl-sci-f1a-header.proto sl-sfnsf.proto sl-slot-alloc.proto)
set(PROTOBUF_Headers sl-mac-pdu-tag.pb.h sl-sci-f1a-header.pb.h sl-sfnsf.pb.h sl-slot-alloc.pb.h)
set(PROTOBUF_sources sl-mac-pdu-tag.pb.cc sl-sci-f1a-header.pb.cc sl-sfnsf.pb.cc sl-slot-alloc.pb.cc)


# include(FindProtobuf)
# find_package(Protobuf REQUIRED)
# include_directories(${Protobuf_INCLUDE_DIRS})

# protobuf_generate_cpp(PROTO_SRCS PROTO_HDRS sl-sci-msg.proto)
# protobuf_generate_cpp(PROTOBUF_sources PROTOBUF_Headers ${PROTOBUF_FILELIST})
# protobuf_generate_cpp(PROTO_SRCS PROTO_HDRS EXPORT_MACRO DLL_EXPORT sl-sci-msg.proto)
# protobuf_generate_cpp(PROTO_SRCS PROTO_HDRS DESCRIPTORS PROTO_DESCS sl-sci-msg.proto)
# protobuf_generate_python(PROTO_PY sl-sci-msg.proto)

FOREACH(proto ${PROTOBUF_FILELIST})
    FILE(TO_NATIVE_PATH ${proto} proto_native)
    EXECUTE_PROCESS(COMMAND ${PROTOBUF_PROTOC_EXECUTABLE} --proto_path=${CMAKE_CURRENT_SOURCE_DIR} --cpp_out=${CMAKE_CURRENT_SOURCE_DIR} ${proto_native} 
    RESULT_VARIABLE rv)
    EXECUTE_PROCESS(COMMAND ${PROTOBUF_PROTOC_EXECUTABLE} --proto_path=${CMAKE_CURRENT_SOURCE_DIR} --python_out=/home/xapp-v2x/ ${proto_native} 
    RESULT_VARIABLE rv)
    # Optional, but that can show the user if something have gone wrong with the proto generation 
    IF(${rv})
         MESSAGE("Generation of data model returned ${rv} for proto ${proto_native}")
    ENDIF()
 ENDFOREACH(proto)


 message("Find protobuf")
 find_package(Protobuf REQUIRED)
 include_directories(${Protobuf_INCLUDE_DIRS})
 
 message("Find protobuf in ns3 decode cmakelist ${Protobuf_INCLUDE_DIRS} ${Protobuf_LIBRARIES}")


# add_library(protos ${PROTOBUF_sources} ${PROTOBUF_Headers})
# add_library( proto_shared SHARED ${PROTOBUF_sources} ${PROTOBUF_Headers})
# target_link_libraries(proto_shared PUBLIC protobuf::libprotobuf)
# set_target_properties( proto_shared
#    			        PROPERTIES
#                 # LINK_FLAGS "-Wl,--whole-archive"
#                 OUTPUT_NAME "proto"
#                 SOVERSION 1
#                 VERSION ${major_version}.${minor_version}.${patch_level}
# )
# target_include_directories(proto_shared PUBLIC "src/ns3_decode" PUBLIC "/usr/local/${install_inc}" )
# set (target_list "proto_shared" )
# install( TARGETS ${target_list} EXPORT LibraryConfig
#        LIBRARY  DESTINATION ${install_lib}
#        ARCHIVE  DESTINATION ${install_lib}
#        PUBLIC_HEADER DESTINATION ${install_inc}
# )


# target_link_libraries(protos /usr/lib/x86_64-linux-gnu/libprotobuf.a)

message("Including directories ${PROTOBUF_sources} ${PROTOBUF_Headers}")

# message("Libraries directories ${Protobuf_LIBRARIES} ${Protobuf_LIBRARY} libprotobuf ${CMAKE_CURRENT_SOURCE_DIR}")



add_library( ns3_decode_objects OBJECT ${SOURCES} ${PROTOBUF_sources})
target_compile_definitions(ns3_decode_objects PUBLIC ASN_DISABLE_OER_SUPPORT)

# set(PROTOBUF_LINKER_FLAGS "-lstdc++ -Dprotobuf_MSVC_STATIC_RUNTIME ON")

# SET(CMAKE_EXE_LINKER_FLAGS 
#           "${CMAKE_EXE_LINKER_FLAGS} -Wl,-rpath -Wl,${Protobuf_INCLUDE_DIRS}")

# target_link_libraries(ns3_decode_objects PUBLIC 
#   libproto
# libprotobuf
# )

# target_link_libraries(ns3_decode_objects protobuf::libprotobuf 
    # ${PROTOBUF_LINKER_FLAGS}
    # ${Protobuf_LIBRARIES} ${PROTOBUF_LINKER_FLAGS}
     
    # /usr/include
# )
# target_link_libraries(ns3_decode_objects PUBLIC protobuf::libprotobuf)

target_include_directories (ns3_decode_objects PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>
  # PUBLIC ${Protobuf_INCLUDE_DIRS}
  # PUBLIC /usr/include
  PRIVATE src)

# header files should go into .../include/xfcpp/
if( DEV_PKG )                                   
  install( FILES
    ${HEADERS} ${PROTOBUF_Headers}
    DESTINATION ${install_inc}
    )
endif()
# ---------------------------------------------------------------------------
