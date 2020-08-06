Name:           perl-Finance-Quote
Version:        1.49
Release:        5%{?dist}
Summary:        A Perl module that retrieves stock and mutual fund quotes
License:        GPLv2+
URL:            https://metacpan.org/release/Finance-Quote
Source0:        https://cpan.metacpan.org/modules/by-module/Finance/Finance-Quote-%{version}.tar.gz
Patch0:         0001-FTfunds-updated-to-current-website.patch
BuildArch:      noarch
# Module Build
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter >= 4:5.10.0
BuildRequires:  perl(ExtUtils::MakeMaker)
# Module Runtime
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(CGI)
BuildRequires:  perl(constant)
BuildRequires:  perl(DateTime)
BuildRequires:  perl(DateTime::Format::Strptime)
BuildRequires:  perl(Encode)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(HTML::Parser)
BuildRequires:  perl(HTML::TableExtract)
BuildRequires:  perl(HTML::TokeParser)
BuildRequires:  perl(HTML::TreeBuilder)
BuildRequires:  perl(HTTP::Cookies)
BuildRequires:  perl(HTTP::Headers)
BuildRequires:  perl(HTTP::Request::Common)
BuildRequires:  perl(HTTP::Status)
BuildRequires:  perl(JSON)
BuildRequires:  perl(JSON::Parse)
BuildRequires:  perl(LWP::Protocol::https)
BuildRequires:  perl(LWP::Simple)
BuildRequires:  perl(LWP::UserAgent)
BuildRequires:  perl(Mozilla::CA)
BuildRequires:  perl(POSIX)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(strict)
BuildRequires:  perl(String::Util)
BuildRequires:  perl(Text::Template)
BuildRequires:  perl(Time::Piece)
BuildRequires:  perl(URI)
BuildRequires:  perl(URI::QueryParam)
BuildRequires:  perl(utf8)
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)
# Test Suite
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(feature)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Test::More)
# Runtime
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
This module retrieves stock and mutual fund quotes from various exchanges
using various source.

%prep
%setup -q -n Finance-Quote-%{version}

# Remove BerkeleyDB files shipped by mistake
rm lib/G*
sed -i -e '/^lib\/G/d' MANIFEST

# Remove redundant exec permissions
find lib/ -type f -name '*.pm' -exec chmod -c -x {} \;

# Fix FTfunds (CPAN RT#129586)
%patch0 -p1

# Avoid documentation name clash
cp -p README README.dist

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} -c %{buildroot}

%check
make test

%files
%if 0%{?_licensedir:1}
%license LICENSE
%else
%doc LICENSE
%endif
%doc Change* Documentation/* README.dist
%{perl_vendorlib}/Finance/
%{_mandir}/man3/Finance::Quote.3*
%{_mandir}/man3/Finance::Quote::AEX.3*
%{_mandir}/man3/Finance::Quote::AIAHK.3*
%{_mandir}/man3/Finance::Quote::ASEGR.3*
%{_mandir}/man3/Finance::Quote::ASX.3*
%{_mandir}/man3/Finance::Quote::BMONesbittBurns.3*
%{_mandir}/man3/Finance::Quote::BSERO.3*
%{_mandir}/man3/Finance::Quote::Bourso.3*
%{_mandir}/man3/Finance::Quote::CSE.3*
%{_mandir}/man3/Finance::Quote::Cdnfundlibrary.3*
%{_mandir}/man3/Finance::Quote::Citywire.3*
%{_mandir}/man3/Finance::Quote::Cominvest.3*
%{_mandir}/man3/Finance::Quote::Currencies.3*
%{_mandir}/man3/Finance::Quote::DWS.3*
%{_mandir}/man3/Finance::Quote::Deka.3*
%{_mandir}/man3/Finance::Quote::FTPortfolios.3*
%{_mandir}/man3/Finance::Quote::FTfunds.3*
%{_mandir}/man3/Finance::Quote::Fidelity.3*
%{_mandir}/man3/Finance::Quote::FidelityFixed.3*
%{_mandir}/man3/Finance::Quote::FinanceCanada.3*
%{_mandir}/man3/Finance::Quote::Finanzpartner.3*
%{_mandir}/man3/Finance::Quote::Fool.3*
%{_mandir}/man3/Finance::Quote::GoldMoney.3*
%{_mandir}/man3/Finance::Quote::HEX.3*
%{_mandir}/man3/Finance::Quote::HU.3*
%{_mandir}/man3/Finance::Quote::IndiaMutual.3*
%{_mandir}/man3/Finance::Quote::LeRevenu.3*
%{_mandir}/man3/Finance::Quote::MStaruk.3*
%{_mandir}/man3/Finance::Quote::ManInvestments.3*
%{_mandir}/man3/Finance::Quote::Morningstar.3*
%{_mandir}/man3/Finance::Quote::MorningstarAU.3*
%{_mandir}/man3/Finance::Quote::MorningstarCH.3*
%{_mandir}/man3/Finance::Quote::MorningstarJP.3*
%{_mandir}/man3/Finance::Quote::NZX.3*
%{_mandir}/man3/Finance::Quote::Platinum.3*
%{_mandir}/man3/Finance::Quote::SEB.3*
%{_mandir}/man3/Finance::Quote::TNetuk.3*
%{_mandir}/man3/Finance::Quote::TSP.3*
%{_mandir}/man3/Finance::Quote::TSX.3*
%{_mandir}/man3/Finance::Quote::Tdefunds.3*
%{_mandir}/man3/Finance::Quote::Tdwaterhouse.3*
%{_mandir}/man3/Finance::Quote::Tiaacref.3*
%{_mandir}/man3/Finance::Quote::Troweprice.3*
%{_mandir}/man3/Finance::Quote::Trustnet.3*
%{_mandir}/man3/Finance::Quote::USFedBonds.3*
%{_mandir}/man3/Finance::Quote::Union.3*
%{_mandir}/man3/Finance::Quote::VWD.3*
%{_mandir}/man3/Finance::Quote::YahooJSON.3*
%{_mandir}/man3/Finance::Quote::YahooYQL.3*
%{_mandir}/man3/Finance::Quote::ZA.3*
%{_mandir}/man3/Finance::Quote::ZA_UnitTrusts.3*

%changelog
* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.49-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.49-4
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.49-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.49-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 30 2019 Paul Howarth <paul@city-fan.org> - 1.49-1
- Update to 1.49
  - Alphavantage: Removed Time::HiRes dependency due to mswin32 not supporting
    clock_gettime calls

* Sun Jun 30 2019 Paul Howarth <paul@city-fan.org> - 1.48-1
- Update to 1.48
  - Alphavantage: Add a waiting mechanism to comply with alphavantage use terms
  - Alphavantage: Added support for several stock exchanges and currencies
  - Updated modules: Union, Deka, Indiamutual, ASX, Yahoojson, TSP, AEX, Fool
  - New modules: IEXTrading, MorningstarAU, MorningstarCH, IEXCloud
  - Yahoo: removed modules referring to yahoo API, which yahoo stopped
  - BUGFIX: 'use of uninitialized value' returned by perl could make gnucash
    fail when more than 15 quotes were requested
  - BUGFIX: MS Windows does not support %%T in strftime call
  - Added new documentation files: Release.txt, Hackers-Guide,
    Modules-README.yml
  - We started moving known failing tests into TODO blocks
- Fix FTfunds (CPAN RT#129586)

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.47-6
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.47-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.47-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.47-3
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.47-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Nov 13 2017 Paul Howarth <paul@city-fan.org> - 1.47-1
- Update to 1.47
  - Drop long-obsolete debian directory
  - AlphaVantage:
    - Added support for .IL ⇒ USD currency and division
    - Graceful error catchup
  - Yahoojson:
    - Module adapted to new URL and returned json
  - Use AlphaVantage for currency quotes instead of Yahoo

* Fri Nov 10 2017 Paul Howarth <paul@city-fan.org> - 1.45-1
- Update to 1.45
  - AlphaVantage:
    - More suffix - currency pairs added
    - GBP and GBX divided by 100

* Wed Nov  8 2017 Paul Howarth <paul@city-fan.org> - 1.44-1
- Update to 1.44
  - Added currencies for .SA (Brazil) and .TO (Canada/Toronto) markets
  - Set up a pause of .7s between queries in AlphaVantage.pm to limit queries

* Tue Nov  7 2017 Paul Howarth <paul@city-fan.org> - 1.43-1
- Update to 1.43
  - More tests in alphavantage.t
  - Bug resolved: removed time from $last_refresh when markets are open
  - Added currency for .DE market
  - Bugfix in currency determination regex

* Mon Nov  6 2017 Paul Howarth <paul@city-fan.org> - 1.41-1
- Update to 1.41
  - Added AlphaVantage module
  - Some other module changes: yahoojson, Morningstar, Bourso, ASX, TSX
    (not working)
- Simplify find command using -delete

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.38-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 06 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.38-5
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.38-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.38-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.38-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Aug 31 2015 Paul Howarth <paul@city-fan.org> - 1.38-1
- Update to 1.38
  - Module updates: tiaacref, yahooJSON, FTfunds, MStaruk, USFedBonds, GoldMoney
  - New modules: fidelityfixed, yahooYQL
  - Removed modules: MTGox
  - More tests: yahoo_speed.t, tiaacref.t
- Avoid documentation name clash between two README files

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.37-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.37-3
- Perl 5.22 rebuild

* Tue Feb 24 2015 Paul Howarth <paul@city-fan.org> - 1.37-2
- Fix GBX pricing in FTfunds (CPAN RT#99783)
- Fix MStaruk quote retrieval (CPAN RT#99784)

* Mon Feb  2 2015 Paul Howarth <paul@city-fan.org> - 1.37-1
- Update to 1.37
  - MorningstarJP: changed dependency from Date::Calc to DateTime
  - Modified 00-use.t to show more info
  - Remove Crypt::SSLeay dependency in favour of LWP::Protocol::https
  - Updated HU.pm and test file to current website

* Fri Nov 14 2014 Paul Howarth <paul@city-fan.org> - 1.35-1
- Update to 1.35
- Clean up and modernize spec somewhat (can't build for EL < 7 as the module
  requires Mozilla::CA)

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.20-4
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Feb 18 2014 Bill Nottingham <notting@redhat.com> - 1.20-2
- add missing https requires (#859607)

* Mon Feb 17 2014 Bill Nottingham <notting@redhat.com> - 1.20-1
- update to 1.20

* Sun Aug 04 2013 Petr Pisar <ppisar@redhat.com> - 1.17-13
- Perl 5.18 rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.17-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.17-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.17-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 25 2012 Petr Pisar <ppisar@redhat.com> - 1.17-9
- Perl 5.16 rebuild
- Specify all dependencies

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.17-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 1.17-7
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.17-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 12 2011 Bill Nottingham <notting@redhat.com> - 1.17-5
- fix TIAA-CREF (#668935, <amessina@messinet.com>)

* Mon Dec 06 2010 Bill Nottingham <notting@redhat.com> - 1.17-4
- fix buildrequires for F-15

* Sat May 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.17-3
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.17-2
- rebuild against perl 5.10.1

* Mon Nov 23 2009 Bradley Baetz <bbaetz@gmail.com> - 1.17-1
- Update to 1.17
- Add extra BuildRequires needed for tests to pass

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.13-2
Rebuild for new perl

* Wed Sep 26 2007 Bill Nottingham <notting@redhat.com>
- add perl(ExtUtils::MakeMaker) buildreq

* Tue Sep 18 2007 Bill Nottingham <notting@redhat.com>
- fix source download URL

* Fri Aug  3 2007 Bill Nottingham <notting@redhat.com>
- tweak license tag

* Mon Jan  8 2007 Bill Nottingham <notting@redhat.com> - 1.13-1
- update to 1.13

* Thu Sep 14 2006 Bill Nottingham <notting@redhat.com> - 1.11-4
- bump for rebuild

* Mon Apr 10 2006 Bill Nottingham <notting@redhat.com> - 1.11-3
- add buildreq for perl-HTML-TableExtract
- clean up sed

* Mon Apr 10 2006 Bill Nottingham <notting@redhat.com> - 1.11-2
- clean up spec file

* Fri Apr  7 2006 Bill Nottingham <notting@redhat.com> - 1.11-1
- initial packaging
