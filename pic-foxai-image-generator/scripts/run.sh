#!/bin/bash
# FoxAI Image Generator Skill Runner

cd /root/.openclaw/workspace
node foxai_generator.cjs "$@" --count 1
