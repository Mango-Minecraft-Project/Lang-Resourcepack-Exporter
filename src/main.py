import tomllib, json, zipfile, os

def ensure_dir(dir):
    try:
        os.makedirs(dir)
    except:
        pass

PACK_FORMAT_MAP = {
    '1.12.2': 3,
    '1.16.5': 6,
    '1.18.2': 8,
    '1.19.2': 9,
    '1.19.4': 13
}

with open('./src/setting.toml', 'rb') as file:
    SETTING = tomllib.load(file)
RESOURCE_PACK = SETTING["resource-pack"]
FILENAME = RESOURCE_PACK["filename"]

ensure_dir(f'./export/{FILENAME}/assets')
with open(f'./export/{FILENAME}/pack.mcmeta', 'w', encoding='utf-8') as file:
    json.dump({
        "pack": {
            "pack_format": PACK_FORMAT_MAP[SETTING['minecraft-version']],
            "description": RESOURCE_PACK['description']
        }
    }, file, indent=2, ensure_ascii=False)

for filename in os.listdir('./mods'):
    if filename.endswith('.jar'):
        with zipfile.ZipFile(f'./mods/{filename}') as jar_file:
            lang_filename = 'en_us.json'
            
            if SETTING['mod-loader'] == 'forge':
                
                if SETTING['minecraft-version'] != '1.12.2':
                    with jar_file.open('META-INF/mods.toml') as mod_info_file:
                        mod_info_data = tomllib.loads(mod_info_file.read().decode())
                    modid = mod_info_data['mods'][0]['modId']
                
                else:
                    with jar_file.open('mcmod.info') as mod_info_file:
                        mod_info_data = json.load(mod_info_file)
                    modid = mod_info_data[0]['modid']
                    lang_filename = 'en_US.lang'
        
            elif SETTING['mod-loader'] in {'fabric', 'quilt'}:
                with jar_file.open('fabric.mod.json') as mod_info_file:
                    mod_info_data = json.load(mod_info_file)
                modid = mod_info_data['id']
            
            with jar_file.open(f'assets/{modid}/lang/{lang_filename}') as lang_file:
                if lang_filename.endswith('.json'):
                    lang_data = json.load(lang_file)
                else:
                    lang_data = lang_file.read().decode()
            ensure_dir(f'./export/{FILENAME}/assets/{modid}/lang/')
            with open(f'./export/{FILENAME}/assets/{modid}/lang/{lang_filename}', 'w', encoding='utf-8') as export_lang_file:
                if lang_filename.endswith('.json'):
                    json.dump(lang_data, export_lang_file, indent=2, ensure_ascii=False)
                else:
                    export_lang_file.write(lang_data)