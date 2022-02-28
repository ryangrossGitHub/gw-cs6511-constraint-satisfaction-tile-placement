def format_output(result, grid_width, tile_count):
    output_variable_value_maps = []

    for i in range(tile_count):
        if i in result[0]:
            output_variable_value_maps.append({
                'variable': i,
                'value': '1'
            })
        elif i in result[1]:
            output_variable_value_maps.append({
                'variable': i,
                'value': '2'
            })
        else:
            output_variable_value_maps.append({
                'variable': i,
                'value': '3'
            })

    output_variable_value_maps.sort(key=lambda k: k['variable'])

    tile_width = 4
    grid_output = chunks(output_variable_value_maps, int(grid_width / tile_width))

    i = 0
    for column_index in range(int(grid_width / tile_width)):
        for row in grid_output:
            if row[column_index]['value'] == '1':
                print(str(i) + ' 4 OUTER_BOUNDARY')
            elif row[column_index]['value'] == '2':
                print(str(i) + ' 4 EL_SHAPE')
            elif row[column_index]['value'] == '3':
                print(str(i) + ' 4 FULL_BLOCK')
            i += 1


def chunks(original_list, size):
    chunked_list = []
    for i in range(0, len(original_list), size):
        chunked_list.append(original_list[i:i + size])

    return chunked_list
