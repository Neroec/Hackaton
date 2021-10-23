function start(n, maxDistance) {
    // Заводим списки инцедентности
    let list = []; // [ [id, [id_edges]] ]
    for (let i = 0; i < nodes2.length; i++) {
        list.push([i, []]);
    }

    // Заполняем списки инцидентности
    let distance = 0;
    for (let i = 0; i < edges2.length; i++) {
        distance += edges2[i][1];
        for (let j = 3; j < 5; j++) {
            for (let k = 0; k < nodes2.length; k++) {
                if (edges2[i][j][0] == nodes2[k][1][0]
                    && edges2[i][j][1] == nodes2[k][1][1]) {
                    list[k][1].push(i);
                    break;
                }
            }
        }
    }
    maxDistance = distance / n;

    // Заводим списки компонент связности
    let components = []; // [ [length, [id_edges]] ]
    let ready = [];
    let countReady = 0;
    for (let i = 0; i < n; i++) {
        max = 0;
        maxId = 0;
        for (let j = 0; j < edges2.length; j++) {
            if (edges2[j][2] > max) {
                max = edges2[j][2];
                maxId = j;
            }
        }
        components.push([edges2[maxId][1], [maxId]]);
        ready.push(0);
        edges2[maxId][2] = 0;
    }

    // Заполняем списки компонент связности
    while (countReady != n) {
        // Обходим все компоненты
        for (let i = 0; i < components.length; i++) {
            // Пропускаем заполненные компоненты
            if (ready[i] == 1) continue;
            // Обходим все ребра компоненты
            max = 0;
            maxId = -1;
            for (let j = 0; j < components[i][1].length; j++) {
                let id = components[i][1][j];
                // Обходим 2 точки ребра
                for (let k = 3; k < 5; k++) {
                    // Определяем индекс точки
                    let id2 = 0;
                    for (let z = 0; z < nodes2.length; z++) {
                        if (nodes2[z][1][0] == edges2[id][k][0]
                            && nodes2[z][1][1] == edges2[id][k][1]) {
                                id2 = z;
                                break;
                        }
                    }
                    // Обходим все инцидентные ребра
                    for (let c = 0; c < list[id2][1].length; c++) {
                        let id3 = list[id2][1][c];
                        if (edges2[id3][2] > max && edges2[id3][1] + components[i][0] <= maxDistance) {
                            max = edges2[id3][2];
                            maxId = id3;
                        }
                    }
                }
            }
            if (maxId == -1) {
                ready[i] = 1;
                countReady += 1;
            } else {
                components[i][1].push(maxId);
                components[i][0] += edges2[maxId][1];
                edges2[maxId][2] = 0;
            }
        }
    }
    console.log(components);
    return components;
}