
-- Options

newoption {
    trigger = "to",
    value   = "path",
    description = "Set the output location for the generated files",
    default = "."
}

newoption {
    trigger     = "rtti",
    description = "Enable Runtime Type information",
    default     = false,
}

newoption {
    trigger     = "no-exception",
    description = "Disable C++ exception handling",
    default     = false,
}

newoption {
    trigger     = "vector-ext",
    value       = "VERSION",
    description = "Set vector extension version",
    default     = "Default",
    allowed     = {
        { "Default" ,   "" },
        { "avx" ,       "" },
        { "avx2" ,      "" },

        { "sse2" ,      "" },
        { "sse3" ,      "" },
        { "ssse3" ,     "" },
        { "sse4.1" ,    "" },
    }
}

if _OPTIONS["help"] then
    return
end

-- Project definition

workspace "ImGui"

    location        (_OPTIONS["to"])

    configurations  { "Debug", "Release" }
    platforms       { "x32", "x64" }

local   imgui_dir = "imgui-master"
local   imgui_examples_dir = imgui_dir.."/examples"

local   external_libs_dir = imgui_examples_dir.."/libs"

local   glfw_dir = external_libs_dir.."/glfw"

project "OpenGL2_GLFW"
    kind        "ConsoleApp"
    language    "C++"

    includedirs {
        imgui_dir,
        imgui_examples_dir,
        glfw_dir.."/include",
    }

    local project_dir = imgui_examples_dir.."/example_glfw_opengl2"

    files {
        project_dir.."/*.cpp",

        -- ImGui files
        imgui_dir.."/*.cpp",
        imgui_dir.."/*.h",

        imgui_examples_dir.."/imgui_impl_glfw.*",
        imgui_examples_dir.."/imgui_impl_opengl2.*",
    }

    vpaths {
        { ["Common"] = imgui_examples_dir.."/*.*", },
        { ["Sources"] = imgui_examples_dir.."/**.*", },
        { ["ImGui"] = imgui_dir.."/*.*", },
    }

    objdir      (_OPTIONS["to"].."/intermediate/")
    targetdir   (_OPTIONS["to"].."/bin/%{cfg.platform}/%{cfg.buildcfg}")

    warnings "Extra"

    if _OPTIONS["rtti"] then
        rtti "On"
    end

    if _OPTIONS["no-exception"] then
        exceptionhandling "Off"
    end

    vectorextensions(_OPTIONS["vector-ext"])

    filter { "action:vs*" }
        characterset "MBCS"

    filter { "configurations:Debug or action:vs*" }
        symbols "On"

    filter { "configurations:Release" }
        flags {
            "LinkTimeOptimization",
            "NoBufferSecurityCheck"
        }
        optimize "Speed"

    -- Links
    filter { "action:vs*" }
        links { "opengl32" }
    filter { "action:not vs*" }
        links { "GL" }

    filter { "action:vs*" }
        libdirs { glfw_dir.."/".._ACTION.."_%{cfg.platform}/%{cfg.buildcfg}" }
    filter { "system:linux" }
        libdirs { glfw_dir.."/%{cfg.system}_%{cfg.platform}" }

    filter { "system:linux" }
        -- X11 and it' s dependencies are needed by glfw
        links {
            "Xrandr",
            "Xinerama",
            "Xi",
            "Xcursor",
            "Xxf86vm",
            "X11",
            "pthread",
        }
