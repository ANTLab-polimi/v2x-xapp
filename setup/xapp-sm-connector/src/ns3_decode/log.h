#ifndef NS3_LOG_H
#define NS3_LOG_H

#include <iostream>
#include "ns_assert.h"

namespace ns3 {
    #define NS_ASSERT(condition)                          \
    do {                                                \
        (void)sizeof (condition);                       \
        } while (false)

    #define NS_ASSERT_MSG(condition, message)             \
    do {                                                \
      (void)sizeof (condition);                       \
    } while (false)

    #define NS_ASSERT_MSG(condition, message)             \
    do {                                                \
        (void)sizeof (condition);                       \
        } while (false)

    #define NS_LOG_NOOP_FUNC_INTERNAL(msg)           \
    do if (false)                                  \
        {                                            \
        std::clog << "";   \
        } while (false)

    #define NS_LOG_FUNCTION(parameters) \
    NS_LOG_NOOP_FUNC_INTERNAL (parameters)
}

#endif /* NS3_LOG_H */