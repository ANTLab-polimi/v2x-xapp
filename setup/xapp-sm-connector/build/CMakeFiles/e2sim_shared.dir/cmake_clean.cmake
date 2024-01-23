file(REMOVE_RECURSE
  "libe2sim.pdb"
  "libe2sim.so"
  "libe2sim.so.1"
  "libe2sim.so.1.0.0"
)

# Per-language clean rules from dependency scanning.
foreach(lang C CXX)
  include(CMakeFiles/e2sim_shared.dir/cmake_clean_${lang}.cmake OPTIONAL)
endforeach()
