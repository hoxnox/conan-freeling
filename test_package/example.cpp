#include <freeling.h>

#include <string>
#include <iostream>

using namespace std;

freeling::maco_options
my_maco_options(const wstring& lang, const wstring& path)
{
	freeling::maco_options opt(lang);
	opt.UserMapFile     = L"";
	opt.LocutionsFile   = L"";
	opt.AffixFile       = path + L"locucions.dat";
	opt.ProbabilityFile = path + L"probabilitats.dat";
	opt.DictionaryFile  = path + L"dicc.src";
	opt.NPdataFile      = path + L"np.dat";
	opt.PunctuationFile = path + L"../common/punct.dat";
	return opt;
}

int
main(int argc, char* argv[])
{
	freeling::util::init_locale(L"default");
	freeling::tokenizer tk(L"share/freeling/en/tokenizer.dat");
	freeling::splitter  sp(L"share/freeling/en/splitter.dat");
	freeling::maco      morfo(my_maco_options(L"en", L"share/freeling/en/"));
	morfo.set_active_options( //
		false,                // UserMap
		true,                 // NumberDetection
		true,                 // PunctuationDetection
		true,                 // DatesDetection
		true,                 // DictionarySearch
		true,                 // AffixAnalisys
		false,                // CompoundAnalisys
		true,                 // RtokContractions
		false,                // MultiwordsDetection
		true,                 // NERecognition
		false,                // QuantitiesDetection
		true);                // ProbabilityAssignment
	freeling::hmm_tagger tagger(L"share/freeling/en/tagger.dat", true, FORCE_TAGGER);

	wstring              text = L"Dynamic authorization failed for device.";
	list<freeling::word> lw   = tk.tokenize(text);
	if (lw.size() == 0)
		wcout << L"error" << endl;
	list<freeling::sentence> ls = sp.split(lw);
	morfo.analyze(ls);
	tagger.analyze(ls);

	for (list<freeling::sentence>::const_iterator is = ls.begin(); is != ls.end(); ++is)
	{
		for (freeling::sentence::const_iterator w = is->begin(); w != is->end(); ++w)
		{
			wcout << L"word '" << w->get_form() << L"'" << endl;
			wcout << L" Possible analisys: {";
			for (freeling::word::const_iterator a = w->analysis_begin(); a != w->analysis_end();
				 ++a)
			{

				wcout << L" (" << a->get_lemma() << L"," << a->get_tag() << L")";
			}
			wcout << L" }" << endl;
			wcout << L"  Selected analisys: (" << w->get_lemma() << L", " << w->get_tag() << L")"
				  << endl;
		}
		wcout << endl;
	}
	return 0;
}
