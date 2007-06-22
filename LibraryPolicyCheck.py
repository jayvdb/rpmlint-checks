# vim:sw=4:et
#############################################################################
# File          : LibraryPolicyCheck.py
# Package       : rpmlint
# Author        : Richard Guenther
# Purpose       : Verify shared library packaging policy rules
#############################################################################

from Filter import *
import AbstractCheck
import rpm
import re
import commands
import stat
import Config
import os
import string
import Pkg

_policy_legacy_exceptions = (
        "libacl1",
        "libadns1",
        "libaio1",
        "libalut0",
        "libapr-1-0",
        "libapr_dbd_mysql",
        "libapr_dbd_pgsql",
        "libapr_dbd_sqlite3",
        "libaprutil-1-0",
        "libapt-pkg-libc6_6-6-2",
        "libarchive1",
        "libart_lgpl_2-2",
        "libatk-1_0-0",
        "libatm1",
        "libattr1",
        "libauthldap0",
        "libauthmysql0",
        "libauthpgsql0",
        "libauthpipe0",
        "libauthuserdb0",
        "libblocxx4",
        "libbluetooth2",
        "libbotan-1_6_1",
        "libcairo2",
        "libcairomm-1_0-1",
        "libcap1",
        "libcasakwallet1",
        "libc-client2006c1_suse",
        "libccrtp1-1_5-0",
        "libcdaudio1",
        "libcdk4",
        "libcheck0",
        "libchewing3",
        "libchm0",
        "libclalsadrv1",
        "libclthreads2",
        "libclucene0",
        "libclxclient3",
        "libcole2",
        "libcppunit-1_10-2",
        "libdaemon0",
        "libdar4",
        "libdbh-4_5-4",
        "libdb_java-4_3",
        "libdbus-glib-1-2",
        "libdbus-qt-1-1",
        "libdc0",
        "libdm0",
        "libdrm2",
        "libdvbpsi4",
        "libdvdnav4",
"libdvdread3",
        "libebml0",
        "libedit0",
        "libeel-2-2",
        "libefence0",
        "libelf0",
        "libevent-1_3b1",
        "libevolutionglue",
        "libexif12",
        "libexif9",
        "libexif-gtk4",
        "libf2c0",
        "libffi4",
        "libflaim5_2",
        "libFnlib0",
        "libfontenc1",
        "libfreebob0",
        "libfreeradius-client2",
        "libfreetype6",
        "libftgl0",
        "libgadu3",
        "libgalago3",
        "libgalago-gtk1",
        "libganglia1",
        "libgcc_s1",
        "libgconfmm-2_6-1",
        "libgcrypt11",
        "libgdiplus0",
        "libgdome0",
        "libgfortran1",
        "libgfortran2",
        "libghttp1",
        "libgif4",
        "libgimpprint1",
        "libglade-2_0-0",
        "libglademm-2_4-1",
        "libgladesharpglue-2",
        "libgle3",
        "libglibsharpglue-2",
        "libgltt0",
        "libglut3",
        "libGLw1",
        "libgnet-2_0-0",
        "libgnomecanvasmm-2_6-1",
        "libgnomecanvaspixbuf1",
        "libgnomecups-1_0-1",
        "libgnome-desktop-2-2",
        "libgnome-keyring0",
        "libgnomemm-2_6-1",
        "libgnomeprintui-2-2-0",
        "libgnomesharpglue-2",
        "libgnomeuimm-2_6-1",
        "libgomp1",
        "libgpg-error0",
        "libGraphicsMagick++1",
        "libgsfglue",
        "libgssapi2",
        "libgtkgl4",
        "libgtksourceview-1_0-0",
        "libgtkxmhtml1",
        "libhandle1",
        "libhangul0",
        "libHermes1",
        "libICE6",
        "libid3-3_8-3",
        "libid3tag0",
        "libIDL-2-0",
        "libidmef0",
        "libilbc0",
        "libiniparser0",
        "libiterm1",
        "libjack0",
        "libjackasyn0",
        "libjasper1",
        "libjpeg62",
        "libkakasi2",
        "libkdegames5",
        "libkeyutils1",
        "libksba8",
        "libkscan1",
        "libktoblzcheck1",
        "liblash2",
        "liblazy0",
        "libldapcpp0",
        "liblite0",
        "liblo0",
        "libloudmouth-1-0",
        "libltdl3",
        "liblua5_1",
        "liblzo2-2",
        "libMagick++10",
        "libmal0",
        "libmatroska0",
        "libmcrypt4",
        "libmdbodbc0",
        "libmeanwhile1",
        "libmemcache0",
        "libmhash2",
        "libmikmod2",
        "libmng1",
        "libmpcdec3",
        "libmpfr1",
        "libmspack0",
        "libmsrpc0",
        "libmusicbrainz4",
        "libnasl2",
        "libneon24",
        "libneon26",
        "libnet0",
        "libnet6-1_3-0",
        "libnetpbm10",
        "libnfsidmap0",
        "libnl1",
        "libnm_glib0",
        "libnm-novellvpn-properties0",
        "libnm-openvpn-properties0",
        "libnm-vpnc-properties0",
        "libnscd1",
        "libnvtvsimple0",
        "libobjc1",
        "libobjc2",
        "libodbcinstQ1",
        "libofa0",
        "libogg0",
        "liboggz1",
        "liboil-0_3-0",
        "libol-0_3_18",
        "liboop4",
        "libopenal0",
        "libopencdk8",
        "libopenobex1",
        "libopenobex-glib1",
        "libp11-0",
        "libparagui-1_0-0",
        "libpathan3",
        "libpcap0",
        "libpcd2",
        "libpgeasy3",
        "libpopt0",
        "libportaudio2",
        "libpq++4",
        "libpqxx-2_5_5",
        "libpythonize0",
        "libPropList0",
        "libpth20",
        "libqca1",
        "libqnotify0",
        "libqscintilla6",
        "libqtc1",
        "libqtpod0",
        "librdf0",
        "librlog1",
        "librpcsecgss3",
        "libsamplerate0",
        "libsax7",
        "libSDL-1_2-0",
        "libSDL_gfx0",
        "libSDL_image-1_2-0",
        "libSDLmm-0_1-8",
        "libSDL_net-1_2-0",
        "libSDL_Pango1",
        "libSDL_ttf-2_0-0",
        "libsecprog0",
        "libserdisp1",
        "libsexy2",
        "libshout3",
        "libsigc-1_2-5",
        "libsigc-2_0-0",
        "libSM6",
        "libsmbclient0",
        "libsmbsharemodes0",
        "libsndfile1",
        "libsoup-2_2-8",
        "libspandsp0",
        "libspeex1",
        "libstartup-notification-1-0",
        "libstdc++5",
        "libstdc++6",
        "libstroke0",
        "libstunnel",
        "libsvg1",
        "libsvg-cairo1",
        "libswfdec-0_4-2",
        "libsynaptics0",
        "libsysfs2",
        "libtclsqlite3-0",
        "libtelepathy2",
        "libthai0",
        "libtheora0",
        "libtonezone1_0",
        "libtre4",
        "libutempter0",
        "libvigraimpex2",
        "libvisual-0_4-0",
        "libvolume_id0",
        "libvtesharpglue-2",
        "libwnck-1-18",
        "libwnn1",
        "libwx_gtk2u_gl-2_8-0",
        "libx86-1",
        "libXau6",
        "libxclass0_9_2",
        "libxcrypt1",
        "libXdmcp6",
        "libXext6",
        "libxfcegui4-4",
        "libXfixes3",
        "libXiterm1",
        "libxkbfile1",
        "libxklavier11",
        "libxml1",
        "libxml++-2_6-2",
        "libXp6",
        "libXprintUtil1",
        "libxquery-1_2",
        "libXrender1",
        "libXt6",
        "libXv1",
        "liby2storage2",
        "liby2util3",
        "libz1",
        "libzio0",
        "libzrtpcpp-0_9-0",
)

from BinariesCheck import BinaryInfo

def libname_from_soname (soname):
    libname = string.split(soname, '.so.')
    if len(libname) == 2:
        if libname[0][-1:].isdigit():
            libname = string.join(libname, '-')
        else:
            libname = string.join(libname, '')
    else:
        libname = soname[:-3]
    libname = libname.replace('.', '_')
    return libname

class LibraryPolicyCheck(AbstractCheck.AbstractCheck):
    def __init__(self):
        self.map = []
        AbstractCheck.AbstractCheck.__init__(self, "LibraryPolicyCheck")

    def check(self, pkg):
        global _policy_legacy_exceptions

        if pkg.isSource():
            return

        # Only check unsuffixed lib* packages
        if pkg.name.endswith('-devel') or pkg.name.endswith('-doc'):
            return

        files = pkg.files()

        # Search for shared libraries in this package
        libs = set()
        dirs = set()
        reqlibs = set()
        shlib_requires = map(lambda x: string.split(x[0],'(')[0], pkg.requires())
        for f in files:
            if f.find('.so.') != -1 or f.endswith('.so'):
                filename = pkg.dirName() + '/' + f
                try:
                    if stat.S_ISREG(files[f][0]):
                        bi = BinaryInfo(pkg, filename, f, 0)
                        if bi.soname != 0:
                            libs.add(bi.soname)
                            dirs.add(string.join(f.split('/')[:-1], '/'))
                        if bi.soname in shlib_requires:
                            # But not if the library is used by the pkg itself
                            # This avoids program packages with their own private lib
                            # FIXME: we'd need to check if somebody else links to this lib
                            reqlibs.add(bi.soname)
                except:
                    pass
            pass

        std_dirs = dirs.intersection(('/lib', '/lib64', '/usr/lib', '/usr/lib64'))

        # If this is a program package (all libs it provides are
        # required by itself), bail out
        if len(libs.difference(reqlibs)) == 0:
            return

        # If this package should be or should be splitted into shlib
        # package(s)
        if len(libs) > 0 and len(std_dirs) > 0:
            # If the package contains a single shlib, name after soname
            if len(libs) == 1:
                soname = libs.copy().pop()
                libname = libname_from_soname (soname)
                if libname.startswith('lib') and pkg.name != libname:
                    if libname in _policy_legacy_exceptions:
                        printWarning(pkg, 'shlib-legacy-policy-name-error', libname)
                    else:
                        printError(pkg, 'shlib-policy-name-error', libname)

            elif not pkg.name[-1:].isdigit():
                printError(pkg, 'shlib-policy-missing-suffix')
        else:
            return

        # Verify no non-lib stuff is in the package
        dirs = set()
        for f in files.keys():
            if os.path.isdir(pkg.dirName()+f):
                dirs.add(f)
            else:
                sf = string.split(f, '.')
                if os.path.dirname(f)[:len('/usr/include')] == '/usr/include':
                    printError(pkg, 'shlib-policy-devel-file', f)
                if os.path.dirname(f) in std_dirs \
                   and (sf[-1] == 'so' or sf[-1] == 'a' or sf[-1] == 'la') \
                   and not os.path.basename(f) in libs:
                    printError(pkg, 'shlib-policy-devel-file', f)

        # Check for non-versioned directories beyond sysdirs in package
        sysdirs = [ '/lib', '/lib64', '/usr/lib', '/usr/lib64',
                    '/usr/share/doc/packages', '/usr/share' ]
        cdirs = set()
        for sysdir in sysdirs:
            done = set()
            for dir in dirs:
                if dir.startswith(sysdir + '/'):
                    ssdir = string.split(dir[len(sysdir)+1:],'/')[0]
                    if not ssdir[-1].isdigit():
                        cdirs.add(sysdir+'/'+ssdir)
                    done.add(dir)
            dirs = dirs.difference(done)
        map(lambda dir: printError(pkg, 'shlib-policy-nonversioned-dir', dir), cdirs)

check=LibraryPolicyCheck()

if Config.info:
    addDetails(
'shlib-policy-missing-suffix',
"""Your package containing shared libraries does not end in a digit and
should probably be split.""",
'shlib-policy-devel-file',
"""Your shared library package contains development files. Split them into
a -devel subpackage.""",
'shlib-policy-name-error',
"""Your package contains a single shared library but is not named after its SONAME.""",
'shlib-policy-nonversioned-dir',
"""Your shared library package contains non-versioned directories. Those will not
allow to install multiple versions of the package in parallel."""
)
