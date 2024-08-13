# 介绍

- 下载bt文件后，如qbittorrent调用，进行作者分类压缩处理
- 可直接python调用，将当前文件夹中所有匹配为'[]'或'【】'的压缩包进行处理，不要含有其它不需要处理的含有'[]'或'【】'的文件

# zip压缩包

- 适用于Tsuk1ko/nhentai-helper相关下载，格式为zip包，并包含info.json信息
- 相关作者数据取之于info.json中的信息，未找到相关信息从文件名'[作者]'中提取相关信息作为作者信息

# cab压缩包

- 适用于ccloli/E-Hentai-Downloader相关下载，格式为cbz包，并包含info.txt信息
- 在info.txt中提取信息后重新转化为ComicInfo.xml后转为zip压缩包

# ComicInfo.xml

- ComicInfo.xml文件作为通用元数据文件，适用于komga漫画管理器进行相应的数据读取，包含：名字、作者、标签、链接等