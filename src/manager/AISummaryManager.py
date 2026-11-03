import yaml
from google import genai
from google.genai import types

from manager.FileManager import FileManager
from models.AISummaryResponse import AISummaryResponse
from models.Config import Config
from models.NoteEntry import NoteEntry
from models.NoteList import NoteList
from utils.YamlUtils import YamlUtils


class AISummaryManager:
    def __init__(self, config_data: Config, file_manager: FileManager):
        self.file_manager = file_manager
        self.__CLIENT =  genai.Client(
            api_key=config_data.gemini_api_key,
        )
        self.__GENERATION_CONFIG = {
            'max_output_tokens': 65536,
            'thinking_level': 'low',
        }

        self.instructions = """
                You are a programmer. At the end of each working day you made notes in yaml file. In these notes you wrote what you did, what needs to be done and if any problems occurred. Each data entity is marked with exclamation mark. Your notes include different work types: done, in progress and problems. Inside those notes, you add task with their descriptions. Task is labeled as \"TaskName1:TaskDescription; TaskName: TaskDescription;\". Some notes can also be without task name, suck as \"TaskName1: TaskDescription;TaskDescription\" 
                

                Example of input: 
                
                <input>
                    !NoteList
                    notes:
                    - !NoteEntry
                      date: '01. Jan. 2026'
                      done: 'Setup'
                      in_progress: 'neki; Task1: Started with task'
                      problems:
                    - !NoteEntry
                      date: '02. Jan. 2026'
                      done: 'Regular maintenance'
                      in_progress: 'neki; Task1: Working on code; Task2: Started with task'
                      problems: 'Task1: Bug found in production'
                    - !NoteEntry
                      date: '03. Jan. 2026'
                      done: 'Task1: Finished development and testing'
                      in_progress: 'neki; Task2: Working on code'
                      problems:
                </input>
                
                You will have a meeting with your superiors and you need to write report. In this report, you will mention notes, grouped by task names. You need to focus on value that this work adds towards business goals. You will respond with a json format. Tone of your response should be professional and easy to read. Do NOT use repeated words between sentences. Highlights the impact  of the work for the business. 
                
                Example of output:
                
                <output>
                
                [
                    {
                        "task_name": "<name>",
                        "task_description: "<description>"
                    },
                    {
                        "task_name": "",
                        "task_description: "<description>"
                    }
                ]
                
                </output>
                
                Follow these steps:
                
                1. Read and analyze input yaml file
                2. Gather task names
                3. For each task name write a full sentence, summarizing notes. In this summary include all notes from "done", "in_progress" and "problems"
                
                
                Make sure to follow these rules:
                
                - sentences should follow chronological order
                - form complete sentences, do not just copy from input
                - sentences should be easy to follow and read
                - mention task descriptions that do not have task names
                - output should be the same language as input
                
                Do not:
                
                - include malformed run-on statements
                - make things up
                - mention dates in sentences
                - make things up
                
            """

    @staticmethod
    def __get_yaml(note_list: NoteList) -> str:
        yaml.add_representer(NoteList, YamlUtils.note_list_representer)
        yaml.add_representer(NoteEntry, YamlUtils.note_entry_representer)
        return yaml.dump(note_list, allow_unicode=True)

    # TODO: Generate summary for date range
    def generate(self, note_list: NoteList):

        new_note_list = NoteList(note_list.notes[-10:])
        input_yaml = self.__get_yaml(new_note_list)

        model = "gemini-flash-lite-latest"
        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=input_yaml),
                ],
            ),
        ]
        generate_content_config = types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(
                thinking_level=types.ThinkingLevel.MINIMAL,
            ),
            audio_transcription_config=types.AudioTranscriptionConfig(
            ),
            system_instruction=[
                types.Part.from_text(text=self.instructions),
            ],
            response_mime_type="application/json",
            response_json_schema=AISummaryResponse.model_json_schema()
        )

        response = []

        for chunk in self.__CLIENT.models.generate_content_stream(
                model=model,
                contents=contents,
                config=generate_content_config,
        ):
            if text := chunk.text:
                response.append(text)
        return "".join(response)
