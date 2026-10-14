[app]
title = SMBC4
package.name = smbc4
package.domain = org.example
source.dir = .
source.include_exts = py,js,html,css,json,unityweb,vfs,png,xml
source.include_patterns = game/*,game/Build/*,game/TemplateData/*
version = 1.0
requirements = python3,kivy,pyjnius,android
orientation = landscape
fullscreen = 1

android.permissions = INTERNET
android.api = 33
android.minapi = 24
android.archs = arm64-v8a
android.accept_sdk_license = True
android.extra_manifest_application_arguments = manifest_app_args.xml

[buildozer]
log_level = 2
warn_on_root = 1
