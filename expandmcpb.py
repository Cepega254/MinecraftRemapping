#!/usr/bin/python

# "Expand" MCPBukkit source on top of MCP source, applying patches, renaming to csv, etc.
#
# https://github.com/MinecraftForge/MCPBukkit

import shutil, difflib, os, sys

outDir = "/tmp/out"
fmlDir = "../Srg2Source/python/fml"
mcpDir = os.path.join(fmlDir, "mcp")
vanillaSrc = os.path.join(mcpDir, "src/minecraft_server") # decompiled server with srgnames
cbPatches = "../MCPBukkit/patches"
obc = "../MCPBukkit/src"

print "Copying vanilla source"
if os.path.exists(outDir):
    shutil.rmtree(outDir)
shutil.copytree(vanillaSrc, outDir)
shutil.copytree(os.path.join(obc, "org"), os.path.join(outDir, "org"))

print "Applying CraftBukkit NMS patches"
sys.path.append(os.path.join(fmlDir))
import fml
fml.apply_patches(mcpDir, cbPatches, os.path.join(outDir, "net"))  # .../

sys.path.append(mcpDir)
import runtime.commands
pushd = os.getcwd()
os.chdir(mcpDir)
commands = runtime.commands.Commands()

commands.srcserver = outDir
print "Adding javadoc"
commands.process_javadoc(runtime.commands.SERVER)
print "Renaming srg->csv"
commands.process_rename(runtime.commands.SERVER)

os.chdir(pushd)

