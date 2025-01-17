# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------
# Vulkan CTS
# ----------
#
# Copyright (c) 2015 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#-------------------------------------------------------------------------

import os
import sys
import re

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "..", "scripts"))

from build.common import DEQP_DIR
from khr_util.format import writeInlFile

VULKAN_H	= [
	os.path.join(os.path.dirname(__file__), "src", "vk_video", "vulkan_video_codecs_common.h"),
	os.path.join(os.path.dirname(__file__), "src", "vk_video", "vulkan_video_codec_h264std.h"),
	os.path.join(os.path.dirname(__file__), "src", "vk_video", "vulkan_video_codec_h264std_encode.h"),
	os.path.join(os.path.dirname(__file__), "src", "vk_video", "vulkan_video_codec_h265std.h"),
	os.path.join(os.path.dirname(__file__), "src", "vk_video", "vulkan_video_codec_h264std_decode.h"),
	os.path.join(os.path.dirname(__file__), "src", "vk_video", "vulkan_video_codec_h265std_decode.h"),
	os.path.join(os.path.dirname(__file__), "src", "vulkan_core.h"),
	]
#VULKAN_H	= os.path.join(os.path.dirname(__file__), "src", "vulkan_core.h")
VULKAN_DIR	= os.path.join(os.path.dirname(__file__), "..", "framework", "vulkan")

INL_HEADER = """\
/* WARNING: This is auto-generated file. Do not modify, since changes will
 * be lost! Modify the generating script instead.
 */\
"""

TYPE_SUBSTITUTIONS		= [
	("uint8_t",		"deUint8"),
	("uint16_t",	"deUint16"),
	("uint32_t",	"deUint32"),
	("uint64_t",	"deUint64"),
	("int8_t",		"deInt8"),
	("int16_t",		"deInt16"),
	("int32_t",		"deInt32"),
	("int64_t",		"deInt64"),
	("bool32_t",	"deUint32"),
	("size_t",		"deUintptr"),
]

def readFile (filename):
	with open(filename, 'rt') as f:
		return f.read()

def writeVulkanCHeader (src, filename):
	def gen ():
		dst = re.sub(r'(#include "[^\s,\n}]+")', '', src)

		# Amber is compiled using C++11 but under MSVC __cplusplus macro
		# is incorrectly recognized and this triggers invalid definition
		dst = dst.replace('VK_NULL_HANDLE ((void*)0)','VK_NULL_HANDLE 0')

		for old_type, new_type in TYPE_SUBSTITUTIONS:
			dst = dst.replace(old_type, new_type)
		yield dst
	writeInlFile(filename, INL_HEADER, gen())

if __name__ == "__main__":
	src = ""
	for file in VULKAN_H:
		src += readFile(file)

	writeVulkanCHeader				(src, os.path.join(VULKAN_DIR, "vkVulkan_c.inl"))
